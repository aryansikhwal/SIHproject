import React, { useState } from 'react';
import { Download, Calendar, BarChart3, PieChart, FileText } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, PieChart as RechartsPieChart, Cell, LineChart, Line, Pie } from 'recharts';

const Reports = () => {
  const [selectedReport, setSelectedReport] = useState('attendance');
  const [dateRange, setDateRange] = useState('month');

  // Mock data for different reports
  const attendanceData = [
    { class: '5A', present: 45, absent: 5, total: 50 },
    { class: '5B', present: 42, absent: 8, total: 50 },
    { class: '6A', present: 38, absent: 7, total: 45 },
    { class: '6B', present: 41, absent: 4, total: 45 },
    { class: '7A', present: 35, absent: 10, total: 45 },
    { class: '7B', present: 40, absent: 5, total: 45 },
  ];

  const monthlyTrend = [
    { month: 'Jan', attendance: 88 },
    { month: 'Feb', attendance: 92 },
    { month: 'Mar', attendance: 89 },
    { month: 'Apr', attendance: 94 },
    { month: 'May', attendance: 91 },
    { month: 'Jun', attendance: 87 },
  ];

  const absenteeismData = [
    { name: 'Regular', value: 78, color: '#228B22' },
    { name: 'Occasional', value: 15, color: '#8FBC8F' },
    { name: 'Chronic', value: 7, color: '#FF6B6B' },
  ];

  const dailyAttendance = [
    { day: 'Mon', rate: 94 },
    { day: 'Tue', rate: 89 },
    { day: 'Wed', rate: 97 },
    { day: 'Thu', rate: 91 },
    { day: 'Fri', rate: 93 },
  ];

  const reportTypes = [
    { id: 'attendance', name: 'Attendance Summary', icon: BarChart3 },
    { id: 'monthly', name: 'Monthly Trends', icon: FileText },
    { id: 'absenteeism', name: 'Absenteeism Analysis', icon: PieChart },
    { id: 'daily', name: 'Daily Patterns', icon: Calendar },
  ];

  const exportReport = (format) => {
    alert(`Exporting ${selectedReport} report as ${format.toUpperCase()}...`);
  };

  const renderReportContent = () => {
    switch (selectedReport) {
      case 'attendance':
        return (
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold text-neutral-dark mb-6">Class-wise Attendance Summary</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={attendanceData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="class" stroke="#666" />
                  <YAxis stroke="#666" />
                  <Bar dataKey="present" fill="#228B22" name="Present" radius={4} />
                  <Bar dataKey="absent" fill="#FF6B6B" name="Absent" radius={4} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        );

      case 'monthly':
        return (
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold text-neutral-dark mb-6">Monthly Attendance Trends</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={monthlyTrend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="month" stroke="#666" />
                  <YAxis stroke="#666" />
                  <Line 
                    type="monotone" 
                    dataKey="attendance" 
                    stroke="#228B22" 
                    strokeWidth={3}
                    dot={{ fill: '#228B22', strokeWidth: 2, r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        );

      case 'absenteeism':
        return (
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold text-neutral-dark mb-6">Absenteeism Pattern Analysis</h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <RechartsPieChart>
                    <Pie
                      data={absenteeismData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={120}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {absenteeismData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                  </RechartsPieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex flex-col justify-center space-y-4">
                {absenteeismData.map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                    <div className="flex items-center">
                      <div 
                        className="w-4 h-4 rounded-full mr-3"
                        style={{ backgroundColor: item.color }}
                      ></div>
                      <span className="font-medium text-neutral-dark">{item.name}</span>
                    </div>
                    <span className="text-lg font-bold text-neutral-dark">{item.value}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 'daily':
        return (
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <h3 className="text-xl font-semibold text-neutral-dark mb-6">Daily Attendance Patterns</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={dailyAttendance}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="day" stroke="#666" />
                  <YAxis stroke="#666" />
                  <Bar dataKey="rate" fill="#8FBC8F" radius={8} />
                </BarChart>
              </ResponsiveContainer>
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
            <h1 className="text-3xl font-bold text-neutral-dark mb-2">Reports</h1>
            <p className="text-gray-600">Generate and analyze attendance reports</p>
          </div>
          <div className="mt-4 lg:mt-0 flex flex-col sm:flex-row gap-3">
            <button
              onClick={() => exportReport('csv')}
              className="px-6 py-2 bg-primary-light text-white rounded-2xl hover:bg-primary transition-colors flex items-center gap-2"
            >
              <Download className="h-4 w-4" />
              Export CSV
            </button>
            <button
              onClick={() => exportReport('pdf')}
              className="px-6 py-2 bg-primary text-white rounded-2xl hover:bg-green-700 transition-colors flex items-center gap-2"
            >
              <FileText className="h-4 w-4" />
              Export PDF
            </button>
          </div>
        </div>
      </div>

      {/* Report Controls */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Report Type Selection */}
          <div>
            <label className="block text-sm font-medium text-neutral-dark mb-3">Report Type</label>
            <div className="grid grid-cols-2 gap-2">
              {reportTypes.map((type) => {
                const Icon = type.icon;
                return (
                  <button
                    key={type.id}
                    onClick={() => setSelectedReport(type.id)}
                    className={`p-3 rounded-xl border-2 transition-all flex items-center justify-center text-sm font-medium ${
                      selectedReport === type.id
                        ? 'border-primary bg-primary text-white'
                        : 'border-gray-200 text-neutral-dark hover:border-primary'
                    }`}
                  >
                    <Icon className="h-4 w-4 mr-2" />
                    {type.name}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Date Range Selection */}
          <div>
            <label className="block text-sm font-medium text-neutral-dark mb-3">Date Range</label>
            <div className="space-y-2">
              {['week', 'month', 'quarter', 'year'].map((range) => (
                <button
                  key={range}
                  onClick={() => setDateRange(range)}
                  className={`w-full p-3 rounded-xl border-2 transition-all text-sm font-medium ${
                    dateRange === range
                      ? 'border-primary bg-primary text-white'
                      : 'border-gray-200 text-neutral-dark hover:border-primary'
                  }`}
                >
                  {range.charAt(0).toUpperCase() + range.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-dark text-sm font-medium">Overall Attendance</p>
              <p className="text-2xl font-bold text-primary">91.2%</p>
              <p className="text-xs text-green-600">↑ 2.1% from last month</p>
            </div>
            <BarChart3 className="h-8 w-8 text-primary" />
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-dark text-sm font-medium">Best Performing Class</p>
              <p className="text-2xl font-bold text-primary">6B</p>
              <p className="text-xs text-green-600">95.6% attendance</p>
            </div>
            <PieChart className="h-8 w-8 text-primary" />
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-dark text-sm font-medium">Total Students</p>
              <p className="text-2xl font-bold text-primary">280</p>
              <p className="text-xs text-blue-600">Across 6 classes</p>
            </div>
            <Calendar className="h-8 w-8 text-primary" />
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-dark text-sm font-medium">Chronic Absentees</p>
              <p className="text-2xl font-bold text-red-500">7</p>
              <p className="text-xs text-red-600">Need intervention</p>
            </div>
            <FileText className="h-8 w-8 text-red-500" />
          </div>
        </div>
      </div>

      {/* Report Content */}
      {renderReportContent()}

      {/* Additional Insights */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <h3 className="text-xl font-semibold text-neutral-dark mb-4">Key Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <div className="p-4 bg-green-50 rounded-xl border-l-4 border-green-400">
              <h4 className="font-medium text-green-800">Positive Trends</h4>
              <p className="text-sm text-green-700">
                Overall attendance has improved by 2.1% this month. Wednesday shows the highest attendance rates.
              </p>
            </div>
            <div className="p-4 bg-blue-50 rounded-xl border-l-4 border-blue-400">
              <h4 className="font-medium text-blue-800">Recommendations</h4>
              <p className="text-sm text-blue-700">
                Focus intervention programs on Monday and Friday to improve weekly consistency.
              </p>
            </div>
          </div>
          
          <div className="space-y-3">
            <div className="p-4 bg-yellow-50 rounded-xl border-l-4 border-yellow-400">
              <h4 className="font-medium text-yellow-800">Areas of Concern</h4>
              <p className="text-sm text-yellow-700">
                Class 7A shows declining attendance trend. Immediate intervention required.
              </p>
            </div>
            <div className="p-4 bg-purple-50 rounded-xl border-l-4 border-purple-400">
              <h4 className="font-medium text-purple-800">Seasonal Patterns</h4>
              <p className="text-sm text-purple-700">
                Monsoon season typically shows 5-8% dip in attendance. Plan accordingly.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;
