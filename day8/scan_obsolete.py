"""Scans phase1_source.abap for obsolete / discouraged statements and prints exact line numbers."""
import re, pathlib

SRC = pathlib.Path("phase1_source.abap")
raw = SRC.read_text().splitlines()
clean = ["" if l.lstrip().startswith("*") else l.split('"')[0] for l in raw]
text = "\n".join(clean)

RULES = [  # (regex, statement, modern replacement, severity)
 (r"^\s*CALL\s+METHOD\b", "CALL METHOD", "Functional call: cl_salv_table=>factory( ... )", "Medium"),
 (r"IF_SALV_C_BOOL_SAP=>(TRUE|FALSE)", "IF_SALV_C_BOOL_SAP=>TRUE/FALSE", "abap_true / abap_false (or omit: default is false)", "Low"),
 (r"^\s*(MOVE|COMPUTE|ADD|SUBTRACT|MULTIPLY|DIVIDE)\b", "Legacy assignment/arithmetic", "= and arithmetic expressions, CORRESPONDING #( )", "Low"),
 (r"^\s*CONCATENATE\b", "CONCATENATE", "String template |{ a }{ b }|", "Medium"),
 (r"^\s*DESCRIBE\s+TABLE\b", "DESCRIBE TABLE", "lines( itab )", "Low"),
 (r"^\s*READ\s+TABLE\b", "READ TABLE", "Table expression itab[ key = val ] / line_exists( )", "Low"),
 (r"\b(OCCURS|WITH\s+HEADER\s+LINE)\b", "Header line / OCCURS", "Plain internal table + work area", "High"),
 (r"^\s*TABLES\b", "TABLES statement", "Typed DATA declaration", "High"),
 (r"^\s*ENDSELECT\b", "SELECT ... ENDSELECT", "SELECT ... INTO TABLE @DATA(...)", "Medium"),
 (r"\bSELECT\s+\*", "SELECT *", "List only the needed columns", "Medium"),
 (r"^\s*(FORM|PERFORM)\b", "FORM / PERFORM", "Methods of a local class", "Medium"),
 (r"^\s*REFRESH\b", "REFRESH", "CLEAR itab", "Low"),
]

rows = []
for i, line in enumerate(clean, 1):
    for rx, name, fix, sev in RULES:
        if re.search(rx, line, re.I):
            rows.append((i, line.strip(), name, fix, sev))

for m in re.finditer(r"CATCH[^.]*\.\s*ENDTRY", text, re.I):
    ln = text.count("\n", 0, m.start()) + 1
    rows.append((ln, clean[ln - 1].strip(), "Empty CATCH (errors swallowed)",
                 "Handle it: show MESSAGE lx TYPE 'E' or log it", "Medium"))

if not re.search(r"AUTHORITY-CHECK", text, re.I):
    rows.append((0, "(whole file)", "No AUTHORITY-CHECK", "Add check on M_BEST_EKO / M_BEST_BSA", "High"))

rows.sort()
out = ["# Obsolete / discouraged statement scan", f"Source: {SRC}  ({len(raw)} lines)", "",
       "| Line | Code | Finding | Replacement | Severity |", "|---|---|---|---|---|"]
out += [f"| {r[0] or '-'} | `{r[1]}` | {r[2]} | {r[3]} | {r[4]} |" for r in rows]
out += ["", f"**{len(rows)} findings.** Limitation: only statements at the start of a line are matched."]
pathlib.Path("scan_report.md").write_text("\n".join(out) + "\n")
print("\n".join(out))
