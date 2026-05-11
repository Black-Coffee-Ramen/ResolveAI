import React, { useState } from "react";

const TicketForm = ({ onTicketCreated }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title || !description) {
      setError("⚠️ Title and description are required.");
      return;
    }
    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch("/api/tickets", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, description }),
      });

      if (!response.ok) {
        throw new Error("❌ Failed to create ticket. Please try again.");
      }

      const newTicket = await response.json();
      onTicketCreated(newTicket);
      setTitle("");
      setDescription("");
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-gradient-to-br from-gray-50 to-blue-50 p-8 rounded-lg shadow-md w-full max-w-lg mx-auto border border-gray-200">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
        Submit a New Ticket
      </h2>
      {error && (
        <p className="text-red-500 text-center mb-4 font-medium">{error}</p>
      )}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Title */}
        <div>
          <label
            htmlFor="title"
            className="block text-gray-700 font-medium mb-2"
          >
            Title
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
            placeholder="e.g., Cannot login to my account"
            required
          />
        </div>

        {/* Description */}
        <div>
          <label
            htmlFor="description"
            className="block text-gray-700 font-medium mb-2"
          >
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="5"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
            placeholder="Provide a detailed description. Include any error messages you've seen."
            required
          ></textarea>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-700 shadow-md transition duration-300 disabled:opacity-50"
        >
          {isSubmitting ? "Submitting..." : "Submit Ticket"}
        </button>
      </form>
    </div>
  );
};

export default TicketForm;
