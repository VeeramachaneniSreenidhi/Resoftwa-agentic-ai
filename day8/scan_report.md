# Obsolete / discouraged statement scan
Source: phase1_source.abap  (26 lines)

| Line | Code | Finding | Replacement | Severity |
|---|---|---|---|---|
| - | `(whole file)` | No AUTHORITY-CHECK | Add check on M_BEST_EKO / M_BEST_BSA | High |
| 17 | `CALL METHOD cl_salv_table=>factory` | CALL METHOD | Functional call: cl_salv_table=>factory( ... ) | Medium |
| 19 | `list_display   = IF_SALV_C_BOOL_SAP=>FALSE` | IF_SALV_C_BOOL_SAP=>TRUE/FALSE | abap_true / abap_false (or omit: default is false) | Low |
| 25 | `CATCH cx_salv_msg.` | Empty CATCH (errors swallowed) | Handle it: show MESSAGE lx TYPE 'E' or log it | Medium |

**4 findings.** Limitation: only statements at the start of a line are matched.
