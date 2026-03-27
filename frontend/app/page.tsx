import PlaidLink from "@/components/PlaidLink";
import { Card, Title, Text } from "@tremor/react";
import { ShieldCheck } from "lucide-react";

const USER_ID = "hackathon_user_001"; // Constant for demo

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4">
      <Card className="max-w-md mx-auto p-8 rounded-3xl shadow-2xl border-0 bg-white">
        <div className="flex flex-col items-center text-center space-y-4">
          <div className="bg-blue-50 p-4 rounded-full">
            <ShieldCheck className="w-12 h-12 text-blue-600" />
          </div>
          <Title className="text-3xl font-bold tracking-tight text-slate-900">
            The David Protocol
          </Title>
          <Text className="text-slate-500 text-lg">
            Empowering the 'Credit Invisible' using cash-flow underwriting.
          </Text>
          
          <div className="w-full pt-4">
            <Text className="text-xs text-slate-400 font-medium uppercase tracking-widest mb-2">
              Step 1: Link your financials
            </Text>
            <PlaidLink userId={USER_ID} />
            <Text className="mt-4 text-xs text-slate-400">
              Personal bank data is securely accessed via 256-bit encryption.
            </Text>
          </div>
        </div>
      </Card>
      
      <div className="mt-12 text-slate-400 text-sm font-medium flex items-center gap-4">
        <span>Sandbox Environment</span>
        <div className="w-1 h-1 bg-slate-300 rounded-full" />
        <span>Plaid Powered</span>
      </div>
    </div>
  );
}
