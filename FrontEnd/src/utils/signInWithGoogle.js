
import { auth,googleProvider,signInWithPopup } from "./firebase-config";

export const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    const user = result.user;
    console.log("User Info:", user);
    return user;
  } catch (error) {
    console.log("Google Sign-In Error:", error.message);
  }
};
