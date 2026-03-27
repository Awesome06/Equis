"use client";

import React, { useCallback, useEffect, useState } from "react";
import { usePlaidLink } from "react-plaid-link";
import { useRouter } from "next/navigation";
import { Button } from "@tremor/react";
import { CreditCard } from "lucide-react";

interface Props {
  userId: string;
}

export default function PlaidLink({ userId }: Props) {
  const [token, setToken] = useState<string | null>(null);
  const router = useRouter();

  // 1. Get Link Token from Backend
  useEffect(() => {
    async function createLinkToken() {
      const response = await fetch("http://localhost:8000/api/plaid/create_link_token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId }),
      });
      const data = await response.json();
      setToken(data.link_token);
    }
    createLinkToken();
  }, [userId]);

  // 2. Success Handler: Exchange Token
  const onSuccess = useCallback(
    async (public_token: string) => {
      const response = await fetch("http://localhost:8000/api/plaid/exchange_public_token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ public_token, user_id: userId }),
      });
      const data = await response.json();
      if (data.status === "success") {
        // Sync transactions in background
        fetch("http://localhost:8000/api/plaid/sync_transactions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ item_id: data.item_id }),
        });
        
        // Redirect to Dashboard
        router.push(`/dashboard?userId=${userId}`);
      }
    },
    [userId, router]
  );

  const { open, ready } = usePlaidLink({
    token,
    onSuccess,
  });

  return (
    <Button
      onClick={() => open()}
      disabled={!ready}
      className="mt-6 w-full flex items-center justify-center gap-2 py-3 text-lg font-semibold rounded-xl bg-blue-600 hover:bg-blue-700 transition-all shadow-lg hover:shadow-blue-200"
    >
      <CreditCard className="w-5 h-5" />
      Connect your Bank Account
    </Button>
  );
}
