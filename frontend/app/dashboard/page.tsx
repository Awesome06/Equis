"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import DashboardUI from "@/components/DashboardUI";
import { Card, Text } from "@tremor/react";

export default function DashboardPage() {
  const searchParams = useSearchParams();
  const userId = searchParams.get("userId") || "hackathon_user_001";
  
  const [data, setData] = useState<{ score: number; stats: any } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        // 1. Fetch Score
        const scoreRes = await fetch(`http://localhost:8000/api/ml/score/${userId}`);
        const scoreData = await scoreRes.json();
        
        // 2. Fetch Stats
        const statsRes = await fetch(`http://localhost:8000/api/ml/stats/${userId}`);
        const statsData = await statsRes.json();
        
        setData({ score: scoreData.score, stats: statsData });
        setLoading(false);
      } catch (e) {
        console.error("Fetch error", e);
        setLoading(false);
      }
    }
    fetchData();
  }, [userId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="max-w-xs text-center border-0 shadow-none bg-transparent">
          <Text className="animate-pulse text-lg font-medium text-blue-600">Calculating your score...</Text>
        </Card>
      </div>
    );
  }

  return (
    <DashboardUI 
      score={data?.score || 0} 
      chartData={data?.stats?.chart_data || []} 
      userName="David" 
    />
  );
}
