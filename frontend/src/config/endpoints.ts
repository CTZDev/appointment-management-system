export const BASE_URL = "http://127.0.0.1:8000";

/* AUTH */
export const ENDPOINTS_AUTH = {
  LOGIN: "{BASE_URL}/api/v1/login",
  REGISTER: "{BASE_URL}/api/v1/register",
  PROFILE: "{BASE_URL}/api/v1/profile",
  UPDATE_PROFILE: "{BASE_URL}/api/v1/update_profile",
  USER_DETAIL: "{BASE_URL}/api/v1/detail_user",
  USERS: "{BASE_URL}/api/v1/users",
  ADD_USER: "{BASE_URL}/api/v1/add_user",
  UPDATE_USER: "{BASE_URL}/api/v1/update_user",
  DELETE_USER: "{BASE_URL}/api/v1/delete_user",
  LOGOUT: "{BASE_URL}/api/v1/logout_session",
  CHANGE_PASSWORD: "{BASE_URL}/api/v1/change_password",
  RESET_PASSWORD_REQUEST: "{BASE_URL}/api/v1/reset_password_request",
  RESET_PASSWORD_CONFIRM: "{BASE_URL}/api/v1/reset_password_confirm",
};

/* CORE */
export const DOCTORS_ENDPOINT = "api/v1/doctors";
export const PACIENTS_ENDPOINT = "api/v1/persons";
