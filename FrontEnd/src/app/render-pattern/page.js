"use client";

import React, { useEffect, useState } from "react";

function Child() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    console.log("Use effect from child");
    // setCount((count) => count + 1);
  }, []);
  console.log(`Child rendering child state=${count}  `);

  return (
    <div className="text-5xl min-h-100 w-100 flex justify-center items-center">
      I am Child
    </div>
  );
}

export default function Parent() {
  const [count, setCount] = useState(0);
  const [sharedState, setSharedState] = useState(0);
  useEffect(() => {
    console.log("Use effect from parent");

    setCount((curr) => curr + 1);
  }, []);
  console.log(`Parent rendering parent state=${count}`);
  return (
    <div className="text-5xl min-h-100 w-100 flex justify-center items-center">
      <div>
        I am Parent
        <Child />
      </div>
    </div>
  );
}
