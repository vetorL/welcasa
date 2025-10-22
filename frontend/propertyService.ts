import { Property } from "@/components/PropertyTable";

const API_BASE_URL = "http://localhost:8000";

export const propertyService = {
  async getAll(): Promise<Property[]> {
    const response = await fetch(`${API_BASE_URL}/properties`);
    if (!response.ok) throw new Error("Failed to fetch properties");
    return response.json();
  },

  async create(data: Omit<Property, "id">): Promise<Property> {
    const response = await fetch(`${API_BASE_URL}/properties`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create property");
    return response.json();
  },

  async update(id: number, data: Omit<Property, "id">): Promise<Property> {
    const response = await fetch(`${API_BASE_URL}/properties/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to update property");
    return response.json();
  },

  async delete(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/properties/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to delete property");
  },
};
