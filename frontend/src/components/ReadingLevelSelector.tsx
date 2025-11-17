/**
 * Component for selecting reading comprehension level
 */
import { ReadingLevel, READING_LEVEL_LABELS, READING_LEVEL_DESCRIPTIONS } from '../types';

interface ReadingLevelSelectorProps {
  value: ReadingLevel;
  onChange: (level: ReadingLevel) => void;
  className?: string;
}

export default function ReadingLevelSelector({
  value,
  onChange,
  className = '',
}: ReadingLevelSelectorProps) {
  return (
    <div className={`reading-level-selector ${className}`}>
      <label htmlFor="reading-level" className="block text-sm font-medium text-gray-700 mb-2">
        Reading Level
      </label>
      <select
        id="reading-level"
        value={value}
        onChange={(e) => onChange(e.target.value as ReadingLevel)}
        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 px-4 py-2 border"
      >
        {(Object.keys(READING_LEVEL_LABELS) as ReadingLevel[]).map((level) => (
          <option key={level} value={level}>
            {READING_LEVEL_LABELS[level]}
          </option>
        ))}
      </select>
      <p className="mt-1 text-sm text-gray-500">
        {READING_LEVEL_DESCRIPTIONS[value]}
      </p>
    </div>
  );
}
