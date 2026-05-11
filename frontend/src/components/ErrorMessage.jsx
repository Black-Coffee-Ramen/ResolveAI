import React from 'react';

function ErrorMessage({ message }) {
  return (
    <div className="bg-red-900 border border-red-700 text-white px-4 py-3 rounded-lg my-4">
      {message}
    </div>
  );
}

export default ErrorMessage;
