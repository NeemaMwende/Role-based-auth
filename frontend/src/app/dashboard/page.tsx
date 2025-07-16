'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useRouter } from 'next/navigation';
import Layout from '../../components/Layout';
import DoctorDashboard from '../../components/DoctorDashboard';
import PatientDashboard from '../../components/PatientDashboard';
import NurseDashboard from '../../components/NurseDashboard';
import { authAPI } from '../../lib/api';

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!user) {
      router.push('/');
      return;
    }

    fetchDashboardData();
  }, [user, router]);

  const fetchDashboardData = async () => {
    try {
      const response = await authAPI.getDashboard();
      setDashboardData(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !user) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
        </div>
      </Layout>
    );
  }

  const renderDashboard = () => {
    if (!dashboardData) return null;

    switch (user.role) {
      case 'doctor':
        return <DoctorDashboard data={dashboardData} />;
      case 'patient':
        return <PatientDashboard data={dashboardData} />;
      case 'nurse':
        return <NurseDashboard data={dashboardData} />;
      default:
        return <div>Unknown role</div>;
    }
  };

  return (
    <Layout>
      <div className="px-4 sm:px-6 lg:px-8">
        {renderDashboard()}
      </div>
    </Layout>
  );
}