import React from 'react';
import './EmptyState.css';

const EmptyState = ({ icon: Icon, title, description, actionButton }) => {
  return (
    <div className="empty-state-container">
      <div className="empty-state-icon-wrapper">
        {Icon && <Icon size={48} className="empty-state-icon" />}
      </div>
      <h3 className="empty-state-title">{title}</h3>
      <p className="empty-state-description">{description}</p>
      {actionButton && <div className="empty-state-action">{actionButton}</div>}
    </div>
  );
};

export default EmptyState;
