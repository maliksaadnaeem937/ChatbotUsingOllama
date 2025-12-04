"use client";
import { signInWithGoogle } from "@/utils/signInWithGoogle";
import React, { useEffect, useState } from "react";
import { FcGoogle } from "react-icons/fc";
import { useDispatch, useSelector } from "react-redux";
import { setUser } from "@/store/slices/userSlice.js";
import { useRouter } from "next/navigation";
import {
  FaRobot,
  FaFileAlt,
  FaChartLine,
  FaGlobe,
  FaMagic,
} from "react-icons/fa";
import Loading from "./Loading";

export default function Login() {
  const { userId, isLoading } = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  console.log("child is being rendered");
  useEffect(() => {
    console.log("Set mount true from child");
    setMounted(true);
  }, []);

  useEffect(() => {
    console.log("use effect for push");
    if (userId && !isLoading) {
      router.push("/dashboard");
    }
  }, [userId, router, isLoading]);

  const handleLogin = async () => {
    try {
      const user = await signInWithGoogle();
      dispatch(
        setUser({
          name: user?.displayName||"",
          email: user?.email||"",
          userId: user?.uid||"",
        })
      );
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  // Don't render anything until mounted on client
  if (!mounted || isLoading) {
    return <Loading />;
  }

  if (userId) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-4">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-white opacity-10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white opacity-10 rounded-full blur-3xl"></div>
      </div>

      <div className="relative max-w-5xl w-full grid md:grid-cols-2 gap-8 items-center">
        {/* Left side - Branding & Features */}
        <div className="text-white space-y-6 hidden md:block">
          <div className="flex items-center gap-3 mb-8">
            <FaMagic className="text-4xl" />
            <h1 className="text-4xl font-bold">AI Assistant Hub</h1>
          </div>

          <p className="text-xl text-white/90 mb-8">
            Your all-in-one AI-powered platform for intelligent conversations
            and analysis
          </p>

          <div className="space-y-4">
            <div className="flex items-start gap-4 bg-white/10 backdrop-blur-sm rounded-xl p-4">
              <FaRobot className="text-3xl flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-lg">Personal AI Assistant</h3>
                <p className="text-white/80 text-sm">
                  Get instant answers to any question
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4 bg-white/10 backdrop-blur-sm rounded-xl p-4">
              <FaFileAlt className="text-3xl flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-lg">Document Intelligence</h3>
                <p className="text-white/80 text-sm">
                  Upload and chat with your documents
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4 bg-white/10 backdrop-blur-sm rounded-xl p-4">
              <FaChartLine className="text-3xl flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-lg">Sentiment Analysis</h3>
                <p className="text-white/80 text-sm">
                  Understand emotions and trends
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4 bg-white/10 backdrop-blur-sm rounded-xl p-4">
              <FaGlobe className="text-3xl flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-lg">Website Analysis</h3>
                <p className="text-white/80 text-sm">
                  Extract insights from any webpage
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Right side - Login Card */}
        <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-10">
          {/* Mobile heading */}
          <div className="md:hidden text-center mb-6">
            <div className="flex items-center justify-center gap-2 mb-2">
              <FaMagic className="text-3xl text-purple-500" />
              <h1 className="text-2xl font-bold text-gray-800">
                AI Assistant Hub
              </h1>
            </div>
          </div>

          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-3">Welcome!</h2>
            <p className="text-gray-600">
              Sign in to unlock powerful AI features
            </p>
          </div>

          {/* Features preview for mobile */}
          <div className="md:hidden grid grid-cols-2 gap-3 mb-8">
            <div className="bg-blue-50 rounded-lg p-3 text-center">
              <FaRobot className="text-2xl text-blue-500 mx-auto mb-1" />
              <p className="text-xs text-gray-700 font-medium">AI Chat</p>
            </div>
            <div className="bg-green-50 rounded-lg p-3 text-center">
              <FaFileAlt className="text-2xl text-green-500 mx-auto mb-1" />
              <p className="text-xs text-gray-700 font-medium">Documents</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-3 text-center">
              <FaChartLine className="text-2xl text-purple-500 mx-auto mb-1" />
              <p className="text-xs text-gray-700 font-medium">Sentiment</p>
            </div>
            <div className="bg-yellow-50 rounded-lg p-3 text-center">
              <FaGlobe className="text-2xl text-yellow-500 mx-auto mb-1" />
              <p className="text-xs text-gray-700 font-medium">Websites</p>
            </div>
          </div>

          <button
            className="w-full flex items-center justify-center gap-3 bg-white border-2 border-gray-300 rounded-xl shadow-sm py-4 px-6 hover:bg-gray-50 hover:border-gray-400 transition duration-300 group"
            onClick={handleLogin}
          >
            <FcGoogle className="text-3xl" />
            <span className="text-gray-700 font-semibold text-lg">
              Continue with Google
            </span>
          </button>

          <p className="text-center text-gray-500 text-sm mt-6">
            By continuing, you agree to our Terms of Service and Privacy Policy
          </p>

          {/* Stats */}
          <div className="mt-8 pt-6 border-t border-gray-200 grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-purple-600">10K+</p>
              <p className="text-xs text-gray-600">Active Users</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-purple-600">50K+</p>
              <p className="text-xs text-gray-600">Conversations</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-purple-600">100K+</p>
              <p className="text-xs text-gray-600">Documents</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
