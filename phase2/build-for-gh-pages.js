const fs = require('fs-extra');
const path = require('path');

async function buildForGitHubPages() {
  try {
    // Remove the existing root files that are not needed for the frontend
    const rootFiles = fs.readdirSync('.');
    
    // Copy the built frontend to the root directory
    await fs.copy('./phase2/frontend/out', '.', {
      overwrite: true,
      filter: (src) => {
        // Skip node_modules and other non-frontend files
        return !src.includes('node_modules') && 
               !src.includes('.git') && 
               !src.includes('phase2/frontend/node_modules') &&
               !src.includes('phase2/backend');
      }
    });
    
    console.log('Successfully copied built frontend to root directory for GitHub Pages');
  } catch (error) {
    console.error('Error building for GitHub Pages:', error);
    process.exit(1);
  }
}

buildForGitHubPages();