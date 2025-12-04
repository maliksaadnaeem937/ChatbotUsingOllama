"use client";
import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSelector, useDispatch } from "react-redux";
import {
  FaRobot,
  FaFileAlt,
  FaChartLine,
  FaGlobe,
  FaSignOutAlt,
  FaMagic,
} from "react-icons/fa";
import { clearUser } from "@/store/slices/userSlice";
import { signOut } from "firebase/auth";
import { auth } from "@/utils/firebase-config";
import Loading from "./Loading";

export default function Dashboard() {
  const router = useRouter();
  const dispatch = useDispatch();
  const { name, userId, isLoading } = useSelector((state) => state.user);

  // useEffect(() => {
  //   if (!isLoading && !userId) {
  //     router.push("/");
  //   }
  // }, [userId, isLoading, router]);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      dispatch(clearUser());
      router.push("/");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  const features = [
    {
      title: "Personal AI Assistant",
      icon: <FaRobot className="text-5xl text-blue-500" />,
      description: "Ask anything and get instant responses.",
      path: "/chat",
      gradient: "from-blue-500 to-blue-600",
      bgColor: "bg-blue-50",
    },
    {
      title: "Document Intelligence",
      icon: <FaFileAlt className="text-5xl text-green-500" />,
      description: "Upload your files and get insights quickly.",
      path: "/documents",
      gradient: "from-green-500 to-green-600",
      bgColor: "bg-green-50",
    },
    {
      title: "Sentiment Analysis",
      icon: <FaChartLine className="text-5xl text-purple-500" />,
      description: "Understand emotions and trends from text.",
      path: "/sentiment",
      gradient: "from-purple-500 to-purple-600",
      bgColor: "bg-purple-50",
    },
    {
      title: "Website Analysis",
      icon: <FaGlobe className="text-5xl text-yellow-500" />,
      description: "Get insights directly from web pages.",
      path: "/website-analysis",
      gradient: "from-yellow-500 to-yellow-600",
      bgColor: "bg-yellow-50",
    },
  ];

  // // Show loading while checking auth
  // if (isLoading) {
  //   return <Loading />;
  // }

  // // Don't render dashboard if no user
  // if (!userId) {
  //   return null;
  // }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 right-20 w-96 h-96 bg-white opacity-5 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 left-20 w-96 h-96 bg-white opacity-5 rounded-full blur-3xl"></div>
      </div>

      {/* Header */}
      <header className="relative bg-white/10 backdrop-blur-md border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div className="flex items-center gap-3">
              <FaMagic className="text-3xl text-white" />
              <div>
                <h1 className="text-2xl sm:text-3xl font-bold text-white">
                  Welcome back, {name || "User"}! 👋
                </h1>
                <p className="text-white/80 text-sm mt-1">
                  Choose a feature to get started
                </p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-5 py-2.5 bg-white/20 backdrop-blur-sm text-white rounded-xl hover:bg-white/30 transition duration-300 border border-white/30"
            >
              <FaSignOutAlt />
              <span className="font-medium">Logout</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Feature Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {features.map((feature, index) => (
            <div
              key={index}
              onClick={() => router.push(feature.path)}
              className="group bg-white rounded-2xl shadow-xl p-8 flex flex-col items-center text-center hover:scale-105 hover:shadow-2xl transform transition-all duration-300 cursor-pointer"
            >
              <div
                className={`${feature.bgColor} rounded-2xl p-6 mb-4 group-hover:scale-110 transition-transform duration-300`}
              >
                {feature.icon}
              </div>
              <h2 className="text-xl font-bold mb-2 text-gray-800">
                {feature.title}
              </h2>
              <p className="text-gray-600 text-sm">{feature.description}</p>
              <div
                className={`mt-4 w-full h-1 bg-gradient-to-r ${feature.gradient} rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300`}
              ></div>
            </div>
          ))}
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-lg p-6">
            <h3 className="text-white/80 text-sm font-medium uppercase tracking-wide">
              Total Chats
            </h3>
            <p className="text-4xl font-bold text-white mt-3">0</p>
            <div className="mt-2 flex items-center gap-1 text-green-300 text-sm">
              <span>↗</span>
              <span>Ready to start</span>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-lg p-6">
            <h3 className="text-white/80 text-sm font-medium uppercase tracking-wide">
              Documents Analyzed
            </h3>
            <p className="text-4xl font-bold text-white mt-3">0</p>
            <div className="mt-2 flex items-center gap-1 text-green-300 text-sm">
              <span>↗</span>
              <span>Upload your first</span>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-lg p-6">
            <h3 className="text-white/80 text-sm font-medium uppercase tracking-wide">
              Websites Scanned
            </h3>
            <p className="text-4xl font-bold text-white mt-3">0</p>
            <div className="mt-2 flex items-center gap-1 text-green-300 text-sm">
              <span>↗</span>
              <span>Analyze any URL</span>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-lg p-6">
            <h3 className="text-white/80 text-sm font-medium uppercase tracking-wide">
              Sentiment Reports
            </h3>
            <p className="text-4xl font-bold text-white mt-3">0</p>
            <div className="mt-2 flex items-center gap-1 text-green-300 text-sm">
              <span>↗</span>
              <span>Get insights</span>
            </div>
          </div>
        </div>

        {/* Quick Start Section */}
        <div className="mt-12 bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-white mb-4">
            🚀 Quick Start Guide
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <div className="bg-blue-500 text-white rounded-lg w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                1
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">Start a Chat</h3>
                <p className="text-white/70 text-sm">
                  Click on Personal AI Assistant to ask anything
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="bg-green-500 text-white rounded-lg w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                2
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">
                  Upload Documents
                </h3>
                <p className="text-white/70 text-sm">
                  Get instant insights from your PDFs and files
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="bg-purple-500 text-white rounded-lg w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                3
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">
                  Analyze Sentiment
                </h3>
                <p className="text-white/70 text-sm">
                  Understand emotions in any text or conversation
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="bg-yellow-500 text-white rounded-lg w-8 h-8 flex items-center justify-center font-bold flex-shrink-0">
                4
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">Scan Websites</h3>
                <p className="text-white/70 text-sm">
                  Extract key information from any webpage
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
