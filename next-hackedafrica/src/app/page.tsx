import Image from "next/image";

export default async function Home() {
  const country_code = "ZA"
  const res = await fetch(`http://localhost:8001/api/v1/attacks/${country_code}`, {
    method: "GET"
  });

  // Handle not found
  if (res.status == 404) {
    return (
      <h1>Not Found</h1>
    )
  } else if (res.status == 500) {
    return (
      <h1>Server error happened</h1>
    )
  }

  const attacksData = await res.json()
  console.log("AttacksData: ", attacksData)


  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1>Welcome to home of Attacks!</h1>
    </div>
  );
}
