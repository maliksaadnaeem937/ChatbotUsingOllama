"use client"

import React from "react";
import { useEffect } from "react";
import Loading from "../../../components/Loading";
import { useRouter } from "next/navigation";
import { useSelector, useDispatch } from "react-redux";
export default function layout({ children }) {

  const router = useRouter();
  const { userId, isLoading } = useSelector((state) => state.user);
  useEffect(() => {
    if (!isLoading && !userId) {
      router.push("/");
    }
  }, [userId, isLoading, router]);
  if (isLoading) {
    return <Loading />;
  }

  if (!userId) {
    return null;
  }
  return <>{children}</>;
}
