import React from 'react';
import { Users, Calendar, UserX, TrendingUp } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, LineChart, Line } from 'recharts';
import { useLanguage } from '../contexts/LanguageContext';
import Insights from '../components/Insights';
import RFIDScanLogList from '../components/RFIDScanLogList';

const Dashboard = () => {
  const { t } = useLanguage();
  const [statistics, setStatistics] = React.useState({});

  React.useEffect(() => {
    fetch('/api/dashboard')
      .then(res => res.json())
      .then(data => setStatistics(data.statistics));
  }, []);

  // Mock data for charts
  const weeklyData = [
    { day: 'Mon', attendance: 92 },
    { day: 'Tue', attendance: 87 },
    { day: 'Wed', attendance: 95 },
    { day: 'Thu', attendance: 89 },
    { day: 'Fri', attendance: 93 },
  ];

  const monthlyTrend = [
    { month: 'Jan', rate: 88 },
    { month: 'Feb', rate: 92 },
    { month: 'Mar', rate: 89 },
    { month: 'Apr', rate: 94 },
    { month: 'May', rate: 91 },
  ];

  const StatCard = ({ title, value, icon: Icon, color, subtitle }) => (
    <div className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-neutral-dark text-sm font-medium mb-1">{title}</p>
          <p className={`text-3xl font-bold ${color}`}>{value}</p>
          {subtitle && <p className="text-gray-500 text-xs mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-2xl ${color === 'text-primary' ? 'bg-green-100' : 'bg-gray-100'}`}>
          <Icon className={`h-6 w-6 ${color}`} />
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <h1 className="text-3xl font-bold text-neutral-dark mb-2">{t('dashboard')}</h1>
        <p className="text-gray-600">{t('welcomeMessage')}</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title={t('totalStudents')}
          value="248"
          icon={Users}
          color="text-primary"
        />
        <StatCard
          title={t('presentToday')}
          value="234"
          icon={Calendar}
          color="text-primary"
          subtitle={`94.4% ${t('attendanceRate')}`}
        />
        <StatCard
          title={t('absentToday')}
          value="14"
          icon={UserX}
          color="text-red-500"
          subtitle={`5.6% ${t('absentees')}`}
        />
        <StatCard
          title={t('weeklyAverage')}
          value="91.2%"
          icon={TrendingUp}
          color="text-primary"
          subtitle={`+2.1% ${t('fromLastWeek')}`}
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Attendance Chart */}
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold text-neutral-dark mb-4">{t('attendanceOverview')}</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="day" stroke="#666" />
                <YAxis stroke="#666" />
                <Bar dataKey="attendance" fill="#228B22" radius={8} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Monthly Trend Chart */}
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-semibold text-neutral-dark mb-4">{t('monthlyTrends')}</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={monthlyTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="month" stroke="#666" />
                <YAxis stroke="#666" />
                <Line 
                  type="monotone" 
                  dataKey="rate" 
                  stroke="#228B22" 
                  strokeWidth={3}
                  dot={{ fill: '#228B22', strokeWidth: 2, r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <h3 className="text-xl font-semibold text-neutral-dark mb-4">{t('recentActivity')}</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
            <div>
              <p className="font-medium text-neutral-dark">{t('classAttendanceMarked')}</p>
              <p className="text-sm text-gray-600">{t('minutesAgo', '2')}</p>
            </div>
            <span className="px-3 py-1 bg-green-100 text-primary text-sm font-medium rounded-full">
              {t('complete')}
            </span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
            <div>
              <p className="font-medium text-neutral-dark">{t('weeklyReportGenerated')}</p>
              <p className="text-sm text-gray-600">{t('hourAgo', '1')}</p>
            </div>
            <span className="px-3 py-1 bg-blue-100 text-blue-600 text-sm font-medium rounded-full">
              {t('new')}
            </span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
            <div>
              <p className="font-medium text-neutral-dark">{t('newStudentsAdded', '3')}</p>
              <p className="text-sm text-gray-600">{t('yesterday')}</p>
            </div>
            <span className="px-3 py-1 bg-gray-100 text-gray-600 text-sm font-medium rounded-full">
              {t('processed')}
            </span>
          </div>
        </div>
      </div>

      {/* Insights Component */}
      <Insights statistics={statistics} />

      {/* RFID Scan Log List */}
      <RFIDScanLogList />
    </div>
  );
};

export default Dashboard;
