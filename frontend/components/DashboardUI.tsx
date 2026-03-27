"use client";

import React from "react";
import {
  Card,
  DonutChart,
  Title,
  Text,
  Flex,
  BadgeDelta,
  Metric,
  ProgressBar,
} from "@tremor/react";

interface Props {
  score: number;
  chartData: { name: string; value: number }[];
  userName: string;
}

export default function DashboardUI({ score, chartData, userName }: Props) {
  return (
    <main className="p-6 md:p-10 max-w-7xl mx-auto space-y-8">
      <div>
        <Title className="text-3xl font-bold text-slate-900">Financial Insights</Title>
        <Text className="text-slate-500 mt-1">
          Welcome back, <span className="font-semibold text-blue-600">{userName}</span>. Here is your current resilience report.
        </Text>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* KPI Score Card */}
        <Card className="rounded-2xl border-0 shadow-lg bg-white p-8">
          <Flex alignItems="start">
            <div>
              <Text className="text-slate-400 uppercase tracking-wider font-semibold text-xs text-tremor-label">
                Financial Resilience Score
              </Text>
              <Metric className="mt-2 text-5xl font-extrabold text-slate-900">{score}/100</Metric>
            </div>
            <BadgeDelta deltaType={score > 60 ? "increase" : "moderateDecrease"}>
              {score > 60 ? "High Growth" : "At Risk"}
            </BadgeDelta>
          </Flex>
          <div className="mt-8">
            <Flex>
              <Text className="text-slate-500 font-medium">Confidence Level</Text>
              <Text className="text-slate-700 font-bold">{score}%</Text>
            </Flex>
            <ProgressBar value={score} color={score > 60 ? "blue" : "red"} className="mt-3" />
            <Text className="mt-4 text-sm text-slate-400 italic">
              *Based on cash-flow analysis of the last 90 days.
            </Text>
          </div>
        </Card>

        {/* Categorized Spending Chart */}
        <Card className="rounded-2xl border-0 shadow-lg bg-white p-8">
          <Title className="text-slate-900 font-bold">In-Depth Spending Analysis</Title>
          <Text className="mt-1 text-slate-500">Transaction categorization by Gemini AI</Text>
          <DonutChart
            className="mt-8 h-56"
            data={chartData}
            category="value"
            index="name"
            colors={["blue", "cyan", "indigo", "violet", "slate"]}
            variant="donut"
            showLabel={true}
          />
        </Card>
      </div>
      
      {/* Decorative footer */}
      <div className="pt-10 border-t border-slate-200 text-center">
        <Text className="text-slate-400 text-xs">
          The David Protocol Underwriting Engine | Secure & Audited
        </Text>
      </div>
    </main>
  );
}
