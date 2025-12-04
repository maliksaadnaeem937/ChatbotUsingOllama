// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBsAwPsByaFxapNSH6xKBA3T5YrFc2EZwc",
  authDomain: "nextjsauthaisemproject.firebaseapp.com",
  projectId: "nextjsauthaisemproject",
  storageBucket: "nextjsauthaisemproject.firebasestorage.app",
  messagingSenderId: "124157741788",
  appId: "1:124157741788:web:6369c22261fcd4453e4219",
  measurementId: "G-6TRFZSLB9F"
};

const googleProvider = new GoogleAuthProvider();

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth, googleProvider, signInWithPopup, signOut };