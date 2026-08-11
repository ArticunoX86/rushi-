import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Navigate } from 'react-router-dom';

/**
 * PermissionGuard
 * 
 * Wraps UI components and only renders them if the current user has the required permission.
 * If fallback is provided, renders that instead (useful for redirects).
 */
const PermissionGuard = ({ require, children, fallback = null }) => {
  const { user } = useAuth();
  
  if (!user || !user.role) {
    return fallback;
  }

  // System Admin always gets full access
  if (user.role.name === "System Administrator") {
    return <>{children}</>;
  }

  const hasPermission = user.role.permissions?.includes(require);

  if (!hasPermission) {
    return fallback;
  }

  return <>{children}</>;
};

export default PermissionGuard;
