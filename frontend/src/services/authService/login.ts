import { BASE_URL, ENDPOINTS_AUTH } from "../../config/endpoints";
import { User } from "../../types/User";

export const login = async (user: User) => {
  const response = await fetch(`${BASE_URL}/${ENDPOINTS_AUTH.LOGIN}`, {
    method: "POST",
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
    body: JSON.stringify(user),
  });

  if (!response.ok) {
    throw new Error("Something went wrong");
  }
  console.log(response.json());
  return response.json();
};
