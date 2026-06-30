import request from "@/utils/request";

export const getItemHot = () => {
  return request.get("/item/hot");
};

export const getBrandSales = () => {
  return request.get("/brand/sales");
};

export const getUserActive = () => {
  return request.get("/user/active");
};

export const getCategorySales = () => {
  return request.get("/category/sales");
};