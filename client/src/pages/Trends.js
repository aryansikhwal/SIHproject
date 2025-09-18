import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Calendar, Brain, AlertCircle } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer, AreaChart, Area, BarChart, Bar } from 'recharts';

const Trends = () => {
  const [activeTab, setActiveTab] = useState('monthly');

  // Mock data for different trend analyses
  const monthlyData = [
    { month: 'Jan', attendance: 88, target: 90 },
    { month: 'Feb', attendance: 92, target: 90 },
    { month: 'Mar', attendance: 89, target: 90 },
    { month: 'Apr', attendance: 94, target: 90 },
    { month: 'May', attendance: 91, target: 90 },
    { month: 'Jun', attendance: 87, target: 90 },
    { month: 'Jul', attendance: 93, target: 90 },
    { month: 'Aug', attendance: 95, target: 90 },
    { month: 'Sep', attendance: 91, target: 90 },
  ];

  const yearlyData = [
    { year: '2021', attendance: 85, events: 12 },
    { year: '2022', attendance: 88, events: 15 },
    { year: '2023', attendance: 91, events: 18 },
    { year: '2024', attendance: 93, events: 22 },
    { year: '2025', attendance: 91, events: 16 },
  ];

  const seasonalData = [
    { season: 'Spring', attendance: 94, temperature: 25 },
    { season: 'Summer', attendance: 87, temperature: 35 },
    { season: 'Monsoon', attendance: 82, temperature: 28 },
    { season: 'Winter', attendance: 91, temperature: 18 },
  ];

  const predictionData = [
    { month: 'Sep', actual: 91, predicted: 92 },
    { month: 'Oct', actual: null, predicted: 89 },
    { month: 'Nov', actual: null, predicted: 87 },
    { month: 'Dec', actual: null, predicted: 90 },
    { month: 'Jan', actual: null, predicted: 93 },
    { month: 'Feb', actual: null, predicted: 91 },
  ];

  const weeklyPatterns = [
    { day: 'Monday', avg: 87, current: 89 },
    { day: 'Tuesday', avg: 91, current: 88 },
    { day: 'Wednesday', avg: 94, current: 95 },
    { day: 'Thursday', avg: 89, current: 91 },
    { day: 'Friday', avg: 85, current: 87 },
  ];

  const tabs = [
    { id: 'monthly', name: 'Monthly Trends', icon: Calendar },
    { id: 'yearly', name: 'Yearly Trends', icon: TrendingUp },
    { id: 'seasonal', name: 'Seasonal Analysis', icon: AlertCircle },
    { id: 'prediction', name: 'AI Predictions', icon: Brain },
  ];

  const TrendCard = ({ title, value, change, icon: Icon, color }) => (
    <div className="bg-white rounded-2xl p-6 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-neutral-dark">{title}</h3>
        <Icon className={`h-6 w-6 ${color}`} />
      </div>
      <div className="flex items-end justify-between">
        <div>
          <p className={`text-3xl font-bold ${color}`}>{value}</p>
          <p className={`text-sm ${change >= 0 ? 'text-green-600' : 'text-red-600'} flex items-center mt-1`}>
            {change >= 0 ? <TrendingUp className="h-4 w-4 mr-1" /> : <TrendingDown className="h-4 w-4 mr-1" />}
            {Math.abs(change)}% vs last period
          </p>
        </div>
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'monthly':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-xl font-semibold text-neutral-dark mb-6">Monthly Attendance Trends</h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={monthlyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="month" stroke="#666" />
                    <YAxis stroke="#666" domain={['dataMin - 5', 'dataMax + 5']} />
                    <Line 
                      type="monotone" 
                      dataKey="attendance" 
                      stroke="#228B22" 
                      strokeWidth={3}
                      dot={{ fill: '#228B22', strokeWidth: 2, r: 6 }}
                      name="Actual"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="target" 
                      stroke="#8FBC8F" 
                      strokeWidth={2}
                      strokeDasharray="5 5"
                      dot={{ fill: '#8FBC8F', strokeWidth: 2, r: 4 }}
                      name="Target"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-xl font-semibold text-neutral-dark mb-6">Weekly Pattern Analysis</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={weeklyPatterns}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="day" stroke="#666" />
                    <YAxis stroke="#666" />
                    <Bar dataKey="avg" fill="#8FBC8F" name="Average" radius={4} />
                    <Bar dataKey="current" fill="#228B22" name="Current Week" radius={4} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        );

      case 'yearly':
        return (
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold text-neutral-dark mb-6">Yearly Attendance Evolution</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={yearlyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="year" stroke="#666" />
                  <YAxis stroke="#666" />
                  <Area
                    type="monotone"
                    dataKey="attendance"
                    stroke="#228B22"
                    fill="#8FBC8F"
                    fillOpacity={0.6}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-green-50 rounded-xl">
                <h4 className="font-medium text-green-800 mb-1">Best Year</h4>
                <p className="text-2xl font-bold text-green-600">2024</p>
                <p className="text-sm text-green-700">93% average attendance</p>
              </div>
              <div className="p-4 bg-blue-50 rounded-xl">
                <h4 className="font-medium text-blue-800 mb-1">Growth Rate</h4>
                <p className="text-2xl font-bold text-blue-600">+8%</p>
                <p className="text-sm text-blue-700">Over 4 years</p>
              </div>
              <div className="p-4 bg-purple-50 rounded-xl">
                <h4 className="font-medium text-purple-800 mb-1">Target Achievement</h4>
                <p className="text-2xl font-bold text-purple-600">78%</p>
                <p className="text-sm text-purple-700">of years exceeded 90%</p>
              </div>
            </div>
          </div>
        );

      case 'seasonal':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-xl font-semibold text-neutral-dark mb-6">Seasonal Attendance Patterns</h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={seasonalData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="season" stroke="#666" />
                    <YAxis stroke="#666" />
                    <Bar dataKey="attendance" fill="#228B22" radius={8} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {seasonalData.map((season, index) => (
                <div key={index} className="bg-white rounded-2xl p-4 shadow-lg">
                  <h4 className="font-semibold text-neutral-dark mb-2">{season.season}</h4>
                  <p className="text-2xl font-bold text-primary mb-1">{season.attendance}%</p>
                  <p className="text-sm text-gray-600">Avg temp: {season.temperature}°C</p>
                  <div className="mt-3 w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-primary h-2 rounded-full"
                      style={{ width: `${season.attendance}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>

            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-xl font-semibold text-neutral-dark mb-4">Seasonal Insights</h3>
              <div className="space-y-3">
                <div className="p-4 bg-yellow-50 rounded-xl border-l-4 border-yellow-400">
                  <h4 className="font-medium text-yellow-800">Monsoon Impact</h4>
                  <p className="text-sm text-yellow-700">
                    Attendance drops by ~12% during monsoon season due to transportation challenges and weather conditions.
                  </p>
                </div>
                <div className="p-4 bg-green-50 rounded-xl border-l-4 border-green-400">
                  <h4 className="font-medium text-green-800">Spring Peak</h4>
                  <p className="text-sm text-green-700">
                    Highest attendance rates observed in spring with optimal weather and fewer health issues.
                  </p>
                </div>
                <div className="p-4 bg-blue-50 rounded-xl border-l-4 border-blue-400">
                  <h4 className="font-medium text-blue-800">Summer Challenges</h4>
                  <p className="text-sm text-blue-700">
                    High temperatures lead to reduced attendance. Consider adjusting school hours during peak summer.
                  </p>
                </div>
              </div>
            </div>
          </div>
        );

      case 'prediction':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-neutral-dark">AI-Powered Attendance Predictions</h3>
                <div className="flex items-center text-sm text-gray-600">
                  <Brain className="h-4 w-4 mr-1" />
                  ML Model Accuracy: 87.3%
                </div>
              </div>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={predictionData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="month" stroke="#666" />
                    <YAxis stroke="#666" />
                    <Line 
                      type="monotone" 
                      dataKey="actual" 
                      stroke="#228B22" 
                      strokeWidth={3}
                      dot={{ fill: '#228B22', strokeWidth: 2, r: 6 }}
                      name="Actual"
                      connectNulls={false}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="predicted" 
                      stroke="#8FBC8F" 
                      strokeWidth={2}
                      strokeDasharray="8 4"
                      dot={{ fill: '#8FBC8F', strokeWidth: 2, r: 4 }}
                      name="Predicted"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-2xl p-6 shadow-lg">
                <h4 className="text-lg font-semibold text-neutral-dark mb-4">Prediction Factors</h4>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Historical Trends</span>
                    <span className="font-medium">35%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Weather Patterns</span>
                    <span className="font-medium">25%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Academic Calendar</span>
                    <span className="font-medium">20%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Local Events</span>
                    <span className="font-medium">15%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Health Indicators</span>
                    <span className="font-medium">5%</span>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-2xl p-6 shadow-lg">
                <h4 className="text-lg font-semibold text-neutral-dark mb-4">Upcoming Alerts</h4>
                <div className="space-y-3">
                  <div className="p-3 bg-yellow-50 rounded-xl border-l-4 border-yellow-400">
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-yellow-800">November Dip Expected</span>
                      <span className="text-xs text-yellow-600">87%</span>
                    </div>
                    <p className="text-xs text-yellow-700 mt-1">Post-festival attendance decline predicted</p>
                  </div>
                  <div className="p-3 bg-green-50 rounded-xl border-l-4 border-green-400">
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-green-800">January Recovery</span>
                      <span className="text-xs text-green-600">93%</span>
                    </div>
                    <p className="text-xs text-green-700 mt-1">New year motivation boost expected</p>
                  </div>
                  <div className="p-3 bg-blue-50 rounded-xl border-l-4 border-blue-400">
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-blue-800">Weather Impact</span>
                      <span className="text-xs text-blue-600">Monitor</span>
                    </div>
                    <p className="text-xs text-blue-700 mt-1">Heavy rainfall warning for next week</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-neutral-dark mb-2">Trends Analysis</h1>
            <p className="text-gray-600">AI-powered insights and attendance predictions</p>
          </div>
          <div className="mt-4 lg:mt-0 flex items-center space-x-2 text-sm text-gray-600">
            <Brain className="h-4 w-4" />
            <span>Last updated: {new Date().toLocaleDateString()}</span>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <TrendCard
          title="Current Trend"
          value="↗ Improving"
          change={2.3}
          icon={TrendingUp}
          color="text-green-600"
        />
        <TrendCard
          title="Best Day"
          value="Wednesday"
          change={5.2}
          icon={Calendar}
          color="text-blue-600"
        />
        <TrendCard
          title="Seasonal Peak"
          value="Spring"
          change={8.1}
          icon={AlertCircle}
          color="text-purple-600"
        />
        <TrendCard
          title="Prediction Accuracy"
          value="87.3%"
          change={1.8}
          icon={Brain}
          color="text-indigo-600"
        />
      </div>

      {/* Tab Navigation */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`p-4 rounded-xl border-2 transition-all flex items-center justify-center text-sm font-medium ${
                  activeTab === tab.id
                    ? 'border-primary bg-primary text-white'
                    : 'border-gray-200 text-neutral-dark hover:border-primary hover:bg-primary-light hover:text-white'
                }`}
              >
                <Icon className="h-4 w-4 mr-2" />
                {tab.name}
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Content */}
      {renderTabContent()}
    </div>
  );
};

export default Trends;
