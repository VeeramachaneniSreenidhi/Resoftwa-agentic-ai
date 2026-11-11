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

