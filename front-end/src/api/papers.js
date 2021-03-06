import request from "@/utils/request";

export function postPaper(data) {
  return request({
    url: "/dms/papers/",
    method: "post",
    headers: {
      "Content-Type": "multipart/form-data",
    },
    data,
  });
}

export function patchPaper(id, data) {
  return request({
    url: `/dms/papers/${id}/`,
    method: "patch",
    headers: {
      "Content-Type": "multipart/form-data",
    },
    data,
  });
}
