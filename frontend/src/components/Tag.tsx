/**
 * Tag/Badge component with pill-shaped design
 */
import React from 'react';

interface TagProps {
  children: React.ReactNode;
  variant?: 'primary' | 'accent' | 'teal' | 'gray';
  icon?: React.ReactNode;
  className?: string;
}

const Tag: React.FC<TagProps> = ({
  children,
  variant = 'gray',
  icon,
  className = '',
}) => {
  const variantClasses = {
    primary: 'tag-primary',
    accent: 'tag-accent',
    teal: 'tag-teal',
    gray: 'tag-gray',
  };

  const classes = [
    'tag',
    variantClasses[variant],
    className,
  ].filter(Boolean).join(' ');

  return (
    <span className={classes}>
      {icon && <span className="mr-1">{icon}</span>}
      {children}
    </span>
  );
};

export default Tag;
