# AttenSync - Automated Attendance System

## 🎯 Overview

AttenSync is a modern, React-based frontend application designed for managing attendance in rural schools. It features an intuitive interface with forest green/matcha green color scheme, comprehensive dashboard, and seamless integration with Flask backend APIs.

## 🚀 Features

### 🏠 Dashboard
- Quick overview cards (Total Students, Present Today, Absent, Weekly Average)
- Interactive charts showing weekly and monthly attendance trends
- Recent activity feed with real-time updates

### 📋 Attendance Management
- Interactive attendance marking with date picker
- Bulk operations (Mark All Present/Absent)
- Real-time search and filtering by class
- CSV export functionality
- Color-coded status indicators

### 👥 Student Management
- Student profile cards with attendance percentages
- Add, edit, and delete student records
- Visual attendance progress bars
- Contact information management
- Class-wise filtering and search

### 📊 Reports & Analytics
- Multiple report types: Attendance Summary, Monthly Trends, Absenteeism Analysis, Daily Patterns
- Interactive charts using Recharts library
- Export functionality (CSV, PDF)
- Key insights and recommendations

### 📈 Trends Analysis
- AI-powered attendance predictions
- Seasonal pattern analysis
- Weekly and yearly trend comparisons
- Weather and event impact analysis
- Predictive alerts and recommendations

### ⚙️ Settings
- School information management
- Teacher profile and security settings
- Notification preferences
- Data synchronization controls
- System information dashboard

## 🎨 Design Features

### Color Scheme
- **Primary**: Forest Green (#228B22) for headers, highlights, action buttons
- **Secondary**: Matcha Green (#8FBC8F) for accents and hover states
- **Background**: White (#FFFFFF) and Light Gray (#F5F5F5)
- **Text**: Dark Gray (#333333)

### UI/UX Elements
- Rounded corners (rounded-2xl) for modern look
- Soft shadows and hover animations
- Responsive grid layouts
- Mobile-friendly collapsible sidebar
- Custom scrollbars with green theme
- Smooth transitions and animations

## 🛠️ Tech Stack

- **Frontend**: React 18
- **Styling**: Tailwind CSS 3.x
- **Charts**: Recharts
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **UI Components**: Headless UI

## 📱 Responsive Design

- **Desktop**: Full sidebar navigation with main content area
- **Tablet**: Collapsible sidebar with responsive grid layouts
- **Mobile**: Bottom navigation bar, optimized card layouts

## 🔗 API Integration

The application is designed to connect with a Flask backend through REST APIs:

### Endpoints Structure
```
/api/attendance      - Fetch & manage attendance records
/api/students        - Student CRUD operations
/api/reports         - Generate various reports
/api/trends          - Trend analysis and predictions
/api/settings        - Application configuration
/api/auth           - Authentication endpoints
```

### Key Features
- Automatic token management
- Error handling and retry logic
- Request/response interceptors
- Health check functionality

## 🚀 Installation & Setup

1. **Prerequisites**
   ```bash
   Node.js >= 14.x
   npm >= 6.x
   ```

2. **Clone and Install**
   ```bash
   cd attensync-frontend
   npm install
   ```

3. **Environment Setup**
   Create `.env` file:
   ```
   REACT_APP_API_URL=http://localhost:5000
   ```

4. **Start Development Server**
   ```bash
   npm start
   ```

5. **Build for Production**
   ```bash
   npm run build
   ```

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Navbar.js       # Top navigation bar
│   └── Sidebar.js      # Side navigation menu
├── pages/              # Main application pages
│   ├── Dashboard.js    # Dashboard with overview
│   ├── Attendance.js   # Attendance management
│   ├── Students.js     # Student management
│   ├── Reports.js      # Reports and analytics
│   ├── Trends.js       # Trend analysis
│   └── Settings.js     # Application settings
├── services/           # API integration
│   └── api.js         # API service functions
├── App.js             # Main application component
├── App.css            # Custom styles
└── index.css          # Global styles with Tailwind
```

## 🌟 Key Components

### Dashboard
- Real-time statistics cards
- Interactive charts (Bar, Line, Area)
- Recent activity timeline
- Color-coded metrics

### Attendance Interface
- Date-based attendance viewing
- One-click attendance marking
- Bulk operations support
- Export functionality

### Student Management
- Card-based student profiles
- Progress tracking visualization
- Contact information display
- Attendance percentage indicators

### Reports System
- Multiple chart types
- Dynamic data filtering
- Export capabilities
- Insights and recommendations

### Trends Analysis
- Predictive modeling display
- Seasonal pattern visualization
- Multi-dimensional analysis
- Alert system for attendance issues

## 🔧 Configuration

### Tailwind Configuration
Custom color palette and extensions in `tailwind.config.js`:
```javascript
colors: {
  primary: {
    DEFAULT: '#228B22',  // Forest Green
    light: '#8FBC8F',    // Matcha Green
  },
  neutral: {
    light: '#F5F5F5',    // Light gray
    dark: '#333333',     // Dark gray
  }
}
```

### PostCSS Setup
Configured for Tailwind CSS integration with autoprefixer support.

## 🔒 Security Features

- JWT token management
- Automatic session handling
- Secure API communication
- Role-based access control ready
- Input validation and sanitization

## 📱 Mobile Optimization

- Touch-friendly interface
- Responsive breakpoints
- Optimized for rural connectivity
- Progressive loading
- Offline capability ready

## 🌐 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check documentation in `/docs` folder

## 🙏 Acknowledgments

- React team for the amazing framework
- Tailwind CSS for the utility-first approach
- Recharts for beautiful chart components
- Lucide React for clean, consistent icons
- SIH 2025 for the opportunity to build this solution

---

**AttenSync** - Bringing modern technology to rural education, one attendance record at a time. 🌱📚
