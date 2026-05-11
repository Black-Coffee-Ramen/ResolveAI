import React from 'react';

function Loader() {
  return (
    <div className="flex justify-center my-8">
      <div className="border-t-4 border-blue-500 border-b-4 border-gray-700 rounded-full w-12 h-12 animate-spin"></div>
    </div>
  );
}

export default Loader;
