import React from 'react';
import '../App.css';

const Modal = ({
  isOpen,
  title,
  onClose,
  onSubmit,
  children,
  submitLabel = 'Save',
  loading = false
}) => {
  return (
    <div className={`modal ${isOpen ? 'open' : ''}`}>
      {isOpen && (
        <div className="modal-content">
          <div className="modal-header">
            <h2 className="modal-title">{title}</h2>
            <button
              className="modal-close"
              onClick={onClose}
              disabled={loading}
            >
              ×
            </button>
          </div>
          
          <form onSubmit={onSubmit}>
            {children}
            
            <div className="form-actions">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={onClose}
                disabled={loading}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Saving...' : submitLabel}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default Modal;
