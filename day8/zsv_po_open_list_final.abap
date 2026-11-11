REPORT zsv_po_open_list.

TYPES ty_t_lifnr TYPE RANGE OF ekko-lifnr.
TYPES ty_t_bedat TYPE RANGE OF ekko-bedat.

CLASS lcl_po_open_list DEFINITION FINAL.
  PUBLIC SECTION.
    TYPES: BEGIN OF ty_po_item,
             ebeln TYPE ekko-ebeln,
             lifnr TYPE ekko-lifnr,
             bedat TYPE ekko-bedat,
             ebelp TYPE ekpo-ebelp,
             matnr TYPE ekpo-matnr,
             menge TYPE ekpo-menge,
             meins TYPE ekpo-meins,
           END OF ty_po_item,
           ty_t_po_item TYPE STANDARD TABLE OF ty_po_item WITH EMPTY KEY.

    METHODS get_po_items
      IMPORTING it_lifnr        TYPE ty_t_lifnr
                it_bedat        TYPE ty_t_bedat
      RETURNING VALUE(rt_items) TYPE ty_t_po_item.

    METHODS display
      IMPORTING it_items TYPE ty_t_po_item
      RAISING   cx_salv_msg.
ENDCLASS.

CLASS lcl_po_open_list IMPLEMENTATION.
  METHOD get_po_items.
    SELECT a~ebeln, a~lifnr, a~bedat,
           b~ebelp, b~matnr, b~menge, b~meins
      FROM ekko AS a
      INNER JOIN ekpo AS b ON b~ebeln = a~ebeln
      WHERE a~lifnr IN @it_lifnr
        AND a~bedat IN @it_bedat
      ORDER BY a~ebeln, b~ebelp
      INTO TABLE @rt_items.
  ENDMETHOD.

  METHOD display.
    DATA(lt_items) = it_items.
    cl_salv_table=>factory(
      IMPORTING r_salv_table = DATA(lo_alv)
      CHANGING  t_table      = lt_items ).
    lo_alv->display( ).
  ENDMETHOD.
ENDCLASS.

DATA: lv_lifnr TYPE elifn,
      lv_bedat TYPE ebdat.
SELECT-OPTIONS: s_lifnr FOR lv_lifnr,
                s_bedat FOR lv_bedat.

START-OF-SELECTION.
  DATA(lo_report) = NEW lcl_po_open_list( ).
  DATA(lt_po) = lo_report->get_po_items( it_lifnr = s_lifnr[]
                                         it_bedat = s_bedat[] ).
  IF lt_po IS INITIAL.
    " TODO: move this text to a message class / text symbol
    MESSAGE 'No purchase orders found for the selection' TYPE 'S' DISPLAY LIKE 'W'.
    RETURN.
  ENDIF.
  TRY.
      lo_report->display( lt_po ).
    CATCH cx_salv_msg INTO DATA(lx_salv).
      MESSAGE lx_salv TYPE 'E'.
  ENDTRY.

*----------------------------------------------------------------------*
* ABAP Unit tests for LCL_PO_OPEN_LIST (selection logic only).
* DB access is replaced by test doubles (CL_OSQL_TEST_ENVIRONMENT).
* The ALV display is a UI call and is intentionally not unit tested.
*----------------------------------------------------------------------*
CLASS ltc_po_open_list DEFINITION FINAL FOR TESTING
  RISK LEVEL HARMLESS DURATION SHORT.

  PRIVATE SECTION.
    CONSTANTS:
      c_v1 TYPE ekko-lifnr VALUE '0000100001',
      c_v2 TYPE ekko-lifnr VALUE '0000100002'.

    CLASS-DATA go_env TYPE REF TO if_osql_test_environment.
    DATA mo_cut TYPE REF TO lcl_po_open_list.

    CLASS-METHODS class_setup.
    CLASS-METHODS class_teardown.
    METHODS setup.
    METHODS teardown.
    METHODS given_po
      IMPORTING iv_ebeln TYPE ekko-ebeln
                iv_lifnr TYPE ekko-lifnr
                iv_bedat TYPE ekko-bedat
                iv_items TYPE i DEFAULT 1.

    " happy path
    METHODS returns_all_without_filter FOR TESTING.
    METHODS filters_by_supplier        FOR TESTING.
    METHODS filters_by_date_range      FOR TESTING.
    " boundaries
    METHODS date_boundary_is_inclusive FOR TESTING.
    METHODS one_row_per_po_item        FOR TESTING.
    METHODS sorted_by_po_and_item      FOR TESTING.
    " negative / edge
    METHODS unknown_supplier_gives_empty FOR TESTING.
    METHODS po_without_items_is_ignored  FOR TESTING.
    METHODS unit_of_measure_returned     FOR TESTING.
ENDCLASS.

CLASS ltc_po_open_list IMPLEMENTATION.
  METHOD class_setup.
    go_env = cl_osql_test_environment=>create(
               i_dependency_list = VALUE #( ( 'EKKO' ) ( 'EKPO' ) ) ).
  ENDMETHOD.

  METHOD class_teardown.
    go_env->destroy( ).
  ENDMETHOD.

  METHOD setup.
    mo_cut = NEW #( ).
  ENDMETHOD.

  METHOD teardown.
    go_env->clear_doubles( ).
  ENDMETHOD.

  METHOD given_po.
    DATA lt_ekko TYPE STANDARD TABLE OF ekko WITH EMPTY KEY.
    DATA lt_ekpo TYPE STANDARD TABLE OF ekpo WITH EMPTY KEY.
    lt_ekko = VALUE #( ( ebeln = iv_ebeln lifnr = iv_lifnr bedat = iv_bedat ) ).
    DO iv_items TIMES.
      APPEND VALUE #( ebeln = iv_ebeln
                      ebelp = sy-index * 10
                      matnr = |MAT{ sy-index }|
                      menge = 5
                      meins = 'EA' ) TO lt_ekpo.
    ENDDO.
    go_env->insert_test_data( lt_ekko ).
    IF lt_ekpo IS NOT INITIAL.
      go_env->insert_test_data( lt_ekpo ).
    ENDIF.
  ENDMETHOD.

  METHOD returns_all_without_filter.
    " proves: empty selection screen returns every PO item (3 rows)
    given_po( iv_ebeln = '4500000001' iv_lifnr = c_v1 iv_bedat = '20260105' iv_items = 2 ).
    given_po( iv_ebeln = '4500000002' iv_lifnr = c_v2 iv_bedat = '20260210' ).
    DATA(lt_act) = mo_cut->get_po_items( it_lifnr = VALUE #( ) it_bedat = VALUE #( ) ).
    cl_abap_unit_assert=>assert_equals( act = lines( lt_act ) exp = 3
      msg = 'Without filters all 3 items must be returned' ).
  ENDMETHOD.

  METHOD filters_by_supplier.
    " proves: only the chosen supplier's items are returned
    given_po( iv_ebeln = '4500000001' iv_lifnr = c_v1 iv_bedat = '20260105' iv_items = 2 ).
    given_po( iv_ebeln = '4500000002' iv_lifnr = c_v2 iv_bedat = '20260210' ).
    DATA(lt_act) = mo_cut->get_po_items(
      it_lifnr = VALUE #( ( sign = 'I' option = 'EQ' low = c_v1 ) )
      it_bedat = VALUE #( ) ).
    cl_abap_unit_assert=>assert_equals( act = lines( lt_act ) exp = 2
      msg = 'Supplier 1 has 2 items' ).
    LOOP AT lt_act INTO DATA(ls_act).
      cl_abap_unit_assert=>assert_equals( act = ls_act-lifnr exp = c_v1
        msg = 'Only supplier 1 rows expected' ).
    ENDLOOP.
  ENDMETHOD.

  METHOD filters_by_date_range.
    " proves: only POs inside the date range are returned
    given_po( iv_ebeln = '4500000001' iv_lifnr = c_v1 iv_bedat = '20260105' ).
    given_po( iv_ebeln = '4500000002' iv_lifnr = c_v2 iv_bedat = '20260210' ).
    DATA(lt_act) = mo_cut->get_po_items(
      it_lifnr = VALUE #( )
      it_bedat = VALUE #( ( sign = 'I' option = 'BT' low = '20260201' high = '20260228' ) ) ).
    cl_abap_unit_assert=>assert_equals( act = lines( lt_act ) exp = 1
      msg = 'Only the February PO expected' ).
    cl_abap_unit_assert=>assert_equals( act = lt_act[ 1 ]-ebeln exp = '4500000002'
      msg = 'Wrong PO returned' ).
  ENDMETHOD.

  METHOD date_boundary_is_inclusive.
    " proves: a PO dated exactly on the range limit is included
    given_po( iv_ebeln = '4500000001' iv_lifnr = c_v1 iv_bedat = '20260131' ).
    DATA(lt_act) = mo_cut->get_po_items(
      it_lifnr = VALUE #( )
      it_bedat = VALUE #( ( sign = 'I' option = 'BT' low = '20260131' high = '20260131' ) ) ).
    cl_abap_unit_assert=>assert_equals( act = lines( lt_act ) exp = 1
      msg = 'Boundary date must be included' ).
  ENDMETHOD.

  METHOD one_row_per_po_item.
    " proves: a PO with 3 items yields 3 rows (join is item level)
    given_po( iv_ebeln = '4500000001' iv_lifnr = c_v1 iv_bedat = '20260105' iv_items = 3 ).
    DATA(lt_act) = mo_cut->get_po_items( it_lifnr = VALUE #( ) it_bedat = VALUE #( ) ).
    cl_abap_unit_assert=>assert_equals( act = lines( lt_act ) exp = 3
      msg = 'One row per PO item expected' ).
  ENDMETHOD.

  METHOD sorted_by_po_and_item.
    " proves: result is sorted by PO number then item number
    given_po( iv_ebeln = '4500000002' iv_lifnr = c_v2 iv_bedat = '20260210' ).
    given_po( iv_ebeln = '4500000001' iv_lifnr = c_v1 iv_bedat = '20260105' iv_items = 2 ).
    DATA(lt_act) = mo_cut->get_po_items( it_lifnr = VALUE #( ) it_bedat = VALUE #( ) ).
    cl_abap_unit_assert=>assert_equals( act = lt_act[ 1 ]-ebeln exp = '4500000001'
      msg = 'First row must be the lowest PO number' ).
    cl_abap_unit_assert=>assert_equals( act = lt_act[ 2 ]-ebelp exp = '00020'
      msg = 'Second row must be item 20 of the first PO' ).
  ENDMETHOD.

  METHOD unknown_supplier_gives_empty.
    " proves: a supplier with no POs returns an empty table, not an error
    given_po( iv_ebeln = '4500000001' iv_lifnr = c_v1 iv_bedat = '20260105' ).
    DATA(lt_act) = mo_cut->get_po_items(
      it_lifnr = VALUE #( ( sign = 'I' option = 'EQ' low = '0000999999' ) )
      it_bedat = VALUE #( ) ).
    cl_abap_unit_assert=>assert_initial( act = lt_act
      msg = 'No rows expected for an unknown supplier' ).
  ENDMETHOD.

  METHOD po_without_items_is_ignored.
    " proves: a PO header with no items is not returned (inner join)
    given_po( iv_ebeln = '4500000001' iv_lifnr = c_v1 iv_bedat = '20260105' iv_items = 0 ).
    DATA(lt_act) = mo_cut->get_po_items( it_lifnr = VALUE #( ) it_bedat = VALUE #( ) ).
    cl_abap_unit_assert=>assert_initial( act = lt_act
      msg = 'Header without items must not appear' ).
  ENDMETHOD.

  METHOD unit_of_measure_returned.
    " proves: quantity is returned together with its unit
    given_po( iv_ebeln = '4500000001' iv_lifnr = c_v1 iv_bedat = '20260105' ).
    DATA(lt_act) = mo_cut->get_po_items( it_lifnr = VALUE #( ) it_bedat = VALUE #( ) ).
    cl_abap_unit_assert=>assert_equals( act = lt_act[ 1 ]-meins exp = 'EA'
      msg = 'Unit of measure must be returned' ).
    cl_abap_unit_assert=>assert_equals( act = lt_act[ 1 ]-menge exp = 5
      msg = 'Quantity must be returned' ).
  ENDMETHOD.
ENDCLASS.
