import { auth } from "./firebase-config";

export const onAuthStateChangedListener = (callback) => {
  return auth.onAuthStateChanged((user) => {
    callback(user);
  });
};
