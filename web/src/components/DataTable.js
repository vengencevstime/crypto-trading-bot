import React, { useState, useCallback, useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import '../App.css';

const DataTable = ({
  title,
  data,
  columns,
  onAdd,
  onEdit,
  onDelete,
  onRefresh,
  loading,
  error,
  showActions = true
}) => {
  const [columnVisibility, setColumnVisibility] = useState(
    columns.reduce((acc, col) => ({ ...acc, [col.field]: true }), {})
  );
  const [gridApi, setGridApi] = useState(null);
  const [showColumnMenu, setShowColumnMenu] = useState(false);
  const [visibleColumns, setVisibleColumns] = useState(columns);

  const onGridReady = (params) => {
    setGridApi(params.api);
  };

  const handleColumnToggle = (field) => {
    setColumnVisibility(prev => ({
      ...prev,
      [field]: !prev[field]
    }));
  };

  const handleSelectAll = () => {
    const allVisible = Object.values(columnVisibility).every(v => v);
    setColumnVisibility(
      columns.reduce((acc, col) => ({ ...acc, [col.field]: !allVisible }), {})
    );
  };

  // Filter columns based on visibility
  const displayColumns = useMemo(() => {
    return columns.filter(col => columnVisibility[col.field] !== false);
  }, [columns, columnVisibility]);

  const gridColumns = useMemo(() => {
    const allColumns = [...displayColumns];
    
    if (showActions) {
      allColumns.push({
        headerName: 'Actions',
        field: 'actions',
        width: 140,
        sortable: false,
        filter: false,
        cellRenderer: (params) => {
          const isEditable = !params.data.id && !params.data.uuid;
          return (
            <div className="action-buttons">
              <button
                className="btn-edit btn-sm"
                onClick={() => onEdit(params.data)}
                title="Edit"
              >
                ✎ Edit
              </button>
              <button
                className="btn-delete btn-sm"
                onClick={() => {
                  if (window.confirm('Are you sure you want to delete this entry?')) {
                    onDelete(params.data);
                  }
                }}
                title="Delete"
              >
                🗑 Delete
              </button>
            </div>
          );
        }
      });
    }

    return allColumns;
  }, [displayColumns, showActions, onEdit, onDelete]);

  const defaultColDef = {
    filter: 'agTextColumnFilter',
    floatingFilter: true,
    resizable: true,
    sortable: true,
    width: 120
  };

  return (
    <div className="table-container">
      <div className="table-header">
        <h2 className="table-title">{title}</h2>
        <div className="table-actions">
          <div className="column-selector">
            <button
              className="column-selector-btn"
              onClick={() => setShowColumnMenu(!showColumnMenu)}
              title="Select columns to display"
            >
              🔍 Columns
            </button>
            {showColumnMenu && (
              <div className="column-menu">
                <div className="column-menu-item" onClick={handleSelectAll}>
                  <input
                    type="checkbox"
                    checked={Object.values(columnVisibility).every(v => v)}
                    onChange={() => {}}
                  />
                  <label style={{ cursor: 'pointer', flex: 1 }}>Select All</label>
                </div>
                <hr style={{ margin: '0.5rem 0' }} />
                {columns.map(col => (
                  <div
                    key={col.field}
                    className="column-menu-item"
                    onClick={() => handleColumnToggle(col.field)}
                  >
                    <input
                      type="checkbox"
                      checked={columnVisibility[col.field] !== false}
                      onChange={() => {}}
                    />
                    <label style={{ cursor: 'pointer', flex: 1 }}>
                      {col.headerName}
                    </label>
                  </div>
                ))}
              </div>
            )}
          </div>
          <button className="btn btn-primary btn-sm" onClick={onRefresh}>
            🔄 Refresh
          </button>
          <button className="btn btn-primary btn-sm" onClick={onAdd}>
            ➕ Add
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message" style={{ margin: '1rem' }}>
          {error}
        </div>
      )}

      {loading ? (
        <div className="loading">Loading...</div>
      ) : data.length === 0 ? (
        <div className="no-data">
          <div className="empty-icon">📭</div>
          <p>No data available. Click "Add" to create your first entry.</p>
        </div>
      ) : (
        <div className="ag-theme-quartz">
          <AgGridReact
            rowData={data}
            columnDefs={gridColumns}
            defaultColDef={defaultColDef}
            onGridReady={onGridReady}
            pagination={true}
            paginationPageSize={20}
            domLayout="autoHeight"
            suppressDragLeaveHidesColumns={true}
            suppressMoveWhenColumnDragging={true}
            animateRows={true}
          />
        </div>
      )}
    </div>
  );
};

export default DataTable;
