interface DataTableProps {
  columns: string[];
  rows: any[][];
}

function formatCell(value: any): string {
  if (value == null) return "—";
  if (typeof value === "number") return value.toLocaleString();
  return String(value);
}

export function DataTable({ columns, rows }: DataTableProps) {
  if (columns.length === 0) return null;

  if (rows.length === 0) {
    return <p className="data-table-empty">No results returned.</p>;
  }

  return (
    <div className="data-table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, ri) => (
            <tr key={ri}>
              {row.map((cell, ci) => (
                <td
                  key={ci}
                  className={typeof cell === "number" ? "data-table__cell--numeric" : undefined}
                >
                  {formatCell(cell)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
