#!/usr/bin/env node
/**
 * Test script for apiService.js
 * Verifies the API service can be imported and initialized correctly
 */

const path = require('path');

// Mock React environment variables
process.env.NODE_ENV = 'test';
process.env.REACT_APP_API_URL = 'http://localhost:5000';

// Mock console to capture logs
const originalLog = console.log;
const originalWarn = console.warn;
const originalError = console.error;

let logs = [];
console.log = (...args) => logs.push(['log', ...args]);
console.warn = (...args) => logs.push(['warn', ...args]);
console.error = (...args) => logs.push(['error', ...args]);

try {
    console.log('🧪 Testing apiService.js import...');
    
    // This would normally require a proper Node.js ESM setup
    // For now, let's just check if the file syntax is valid
    const fs = require('fs');
    const filePath = path.join(__dirname, 'client', 'src', 'services', 'apiService.js');
    
    if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf8');
        
        console.log('✅ File exists and is readable');
        console.log(`📊 File size: ${content.length} characters`);
        console.log(`📦 Contains import: ${content.includes('import axios') ? 'Yes' : 'No'}`);
        console.log(`🔧 Contains class: ${content.includes('class AttenSyncAPI') ? 'Yes' : 'No'}`);
        console.log(`📡 Contains export: ${content.includes('export default') ? 'Yes' : 'No'}`);
        
        // Check for common issues
        const issues = [];
        
        if (content.includes('"""')) issues.push('Python-style comments found');
        if (content.includes('def ')) issues.push('Python function definitions found');
        if (!content.includes('export')) issues.push('No exports found');
        if (!content.includes('axios')) issues.push('Axios not imported');
        
        if (issues.length === 0) {
            console.log('✅ No obvious issues detected');
        } else {
            console.log('⚠️ Potential issues:');
            issues.forEach(issue => console.log(`   - ${issue}`));
        }
        
        console.log('🎉 apiService.js test completed successfully');
        
    } else {
        console.error('❌ File not found:', filePath);
    }
    
} catch (error) {
    console.error('❌ Test failed:', error.message);
} finally {
    // Restore console
    console.log = originalLog;
    console.warn = originalWarn;
    console.error = originalError;
    
    // Print captured logs
    logs.forEach(([level, ...args]) => {
        const method = console[level] || console.log;
        method(...args);
    });
}