import axios from "axios";

const API_BASE = "http://localhost:8000";

export const detectCoins = async (
  file: File,
  minArea: number,
  circularity: number,
  steps: boolean
) => {
  const formData = new FormData();
  formData.append("file", file);
  const url = steps ? `${API_BASE}/detect/steps` : `${API_BASE}/detect`;
  return axios.post(url, formData, {
    headers: { "Content-Type": "multipart/form-data" },
    params: {
      min_area: minArea,
      circularity_threshold: circularity,
      return_image: steps ? "false" : "true"
    }
  });
};
