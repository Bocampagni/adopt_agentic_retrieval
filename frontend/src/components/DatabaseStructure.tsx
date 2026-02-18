import { useQuery } from "@tanstack/react-query";
import { fetchSchema } from "@/api/chat";

function formatCell(value: any): string {
  if (value == null) return "—";
  if (typeof value === "number") return value.toLocaleString();
  return String(value);
}

export function DatabaseStructure() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["schema"],
    queryFn: fetchSchema,
    staleTime: 5 * 60 * 1000,
  });

  return (
    <main className="db-view">
      <header className="db-view__header">
        <h1 className="db-view__title">Database Structure</h1>
        <p className="db-view__subtitle">
          Preview of the connected data source
        </p>
      </header>

      <div className="db-view__body">
        {isLoading && (
          <div className="db-view__loading">Loading schema...</div>
        )}

        {error && (
          <div className="db-view__error">
            Failed to load schema: {(error as Error).message}
          </div>
        )}

        {data && (
          <div className="db-view__card">
            <div className="db-view__card-header">
              <span className="db-view__table-badge">TABLE</span>
              <h2 className="db-view__table-name">{data.table_name}</h2>
              <span className="db-view__meta">
                {data.columns.length} columns &middot; showing {data.sample_rows.length} rows
              </span>
            </div>

            <div className="db-view__columns">
              <h3 className="db-view__section-title">Columns</h3>
              <div className="db-view__column-grid">
                {data.columns.map((col) => (
                  <span key={col} className="db-view__column-chip">{col}</span>
                ))}
              </div>
            </div>

            <div className="db-view__preview">
              <h3 className="db-view__section-title">Sample Data</h3>
              <div className="data-table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      {data.columns.map((col) => (
                        <th key={col}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.sample_rows.map((row, ri) => (
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
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
