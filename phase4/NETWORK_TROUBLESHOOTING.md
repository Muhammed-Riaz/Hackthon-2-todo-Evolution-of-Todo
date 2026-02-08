# Docker Network Troubleshooting Guide

## 🔴 Current Issue: DNS Resolution Failure

Your Docker setup has a **DNS resolution problem** that's preventing it from connecting to Docker Hub to download base images.

### Diagnostic Results

✅ **Internet Connectivity:** Working (can ping 8.8.8.8)
❌ **DNS Resolution:** Failing (DNS server 1.1.1.1 timing out)
❌ **Docker Hub Access:** Blocked (cannot resolve registry-1.docker.io)

## 🔧 Solutions (Try in Order)

### Solution 1: Configure Docker Desktop DNS (Recommended)

This is the most reliable fix for Docker-specific DNS issues.

**Steps:**

1. **Open Docker Desktop**
   - Click the Docker icon in system tray
   - Click "Settings" (gear icon)

2. **Navigate to Docker Engine**
   - Click "Docker Engine" in left sidebar

3. **Add DNS Configuration**
   - You'll see a JSON configuration
   - Add the `dns` property:

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"],
  "experimental": false
}
```

4. **Apply Changes**
   - Click "Apply & Restart"
   - Wait 30-60 seconds for Docker to restart

5. **Test the Fix**
```bash
docker pull hello-world
```

If successful, you'll see:
```
latest: Pulling from library/hello-world
...
Status: Downloaded newer image for hello-world:latest
```

### Solution 2: Change System DNS Settings

If Docker Desktop DNS configuration doesn't work, change your Windows DNS settings.

**Steps:**

1. **Open Network Settings**
   - Press `Win + R`
   - Type `ncpa.cpl` and press Enter

2. **Configure Network Adapter**
   - Right-click your active network adapter
   - Select "Properties"

3. **Change IPv4 DNS**
   - Select "Internet Protocol Version 4 (TCP/IPv4)"
   - Click "Properties"
   - Select "Use the following DNS server addresses"
   - Preferred DNS: `8.8.8.8`
   - Alternate DNS: `8.8.4.4`
   - Click "OK"

4. **Flush DNS Cache**
```bash
ipconfig /flushdns
```

5. **Test DNS Resolution**
```bash
nslookup registry-1.docker.io
```

Expected output:
```
Server:  google-public-dns-a.google.com
Address:  8.8.8.8

Non-authoritative answer:
Name:    registry-1.docker.io
Addresses:  <IP addresses>
```

### Solution 3: Check Firewall/Antivirus

Your firewall or antivirus might be blocking DNS requests.

**Steps:**

1. **Temporarily Disable Firewall**
   - Windows Defender Firewall → Turn off (temporarily)
   - Test Docker: `docker pull hello-world`

2. **If This Works:**
   - Re-enable firewall
   - Add Docker Desktop to firewall exceptions:
     - Allow: `C:\Program Files\Docker\Docker\resources\com.docker.backend.exe`
     - Allow: `C:\Program Files\Docker\Docker\Docker Desktop.exe`

3. **Check Antivirus**
   - Some antivirus software blocks Docker networking
   - Add Docker to exceptions or temporarily disable

### Solution 4: Use VPN or Different Network

If you're on a corporate or restricted network:

**Options:**

1. **Try Mobile Hotspot**
   - Connect to your phone's hotspot
   - Test Docker connectivity

2. **Use VPN**
   - Connect to a VPN service
   - Test Docker connectivity

3. **Contact Network Administrator**
   - Your network might be blocking Docker Hub
   - Request access to:
     - `registry-1.docker.io` (port 443)
     - `auth.docker.io` (port 443)
     - `production.cloudflare.docker.com` (port 443)

### Solution 5: Use Docker Desktop Proxy Settings

If you're behind a corporate proxy:

**Steps:**

1. **Open Docker Desktop Settings**
   - Go to "Resources" → "Proxies"

2. **Configure Proxy**
   - Enable "Manual proxy configuration"
   - Enter your proxy details:
     - HTTP Proxy: `http://proxy.company.com:8080`
     - HTTPS Proxy: `http://proxy.company.com:8080`
   - Add bypass list if needed

3. **Apply and Restart**

## 🧪 Verification Steps

After applying any solution, run these tests:

### Test 1: DNS Resolution
```bash
nslookup registry-1.docker.io
```
✅ Should return IP addresses

### Test 2: Docker Hub Connectivity
```bash
docker pull hello-world
```
✅ Should download successfully

### Test 3: Build Backend Image
```bash
cd backend
docker build -t todo-backend:latest .
```
✅ Should start downloading Python base image

### Test 4: Build Frontend Image
```bash
cd frontend
docker build -t todo-frontend:latest .
```
✅ Should start downloading Node base image

## 📊 Current Network Status

Based on diagnostics:

| Test | Status | Details |
|------|--------|---------|
| Internet | ✅ Working | Can reach 8.8.8.8 |
| DNS Server | ❌ Failing | 1.1.1.1 timing out |
| Docker Hub | ❌ Blocked | Cannot resolve registry |
| Docker Desktop | ✅ Running | Version 29.2.0 |

## 🎯 Recommended Action Plan

1. **First:** Try Solution 1 (Docker Desktop DNS) - Takes 2 minutes
2. **If fails:** Try Solution 2 (System DNS) - Takes 3 minutes
3. **If fails:** Try Solution 3 (Firewall) - Takes 5 minutes
4. **If fails:** Try Solution 4 (Different Network) - Immediate test
5. **Last resort:** Contact network administrator

## 🔄 After Fixing DNS

Once DNS is working, build your images separately:

### Build Backend Image
```bash
cd backend
docker build -t todo-backend:latest .
```

Expected output:
```
[+] Building 45.2s (12/12) FINISHED
 => [1/6] FROM docker.io/library/python:3.11-slim
 => [2/6] WORKDIR /app
 => [3/6] COPY requirements.txt .
 => [4/6] RUN pip install -r requirements.txt
 => [5/6] COPY . .
 => [6/6] exporting to image
Successfully tagged todo-backend:latest
```

### Build Frontend Image
```bash
cd frontend
docker build -t todo-frontend:latest .
```

Expected output:
```
[+] Building 120.5s (18/18) FINISHED
 => [deps 1/4] FROM docker.io/library/node:20-alpine
 => [deps 2/4] WORKDIR /app
 => [deps 3/4] COPY package.json package-lock.json* ./
 => [deps 4/4] RUN npm ci
 => [builder 1/3] COPY --from=deps /app/node_modules ./node_modules
 => [builder 2/3] COPY . .
 => [builder 3/3] RUN npm run build
Successfully tagged todo-frontend:latest
```

### Verify Both Images
```bash
docker images | grep todo
```

Expected output:
```
todo-backend    latest    abc123def456    2 minutes ago    450MB
todo-frontend   latest    def456ghi789    5 minutes ago    180MB
```

## 📞 Still Having Issues?

If none of these solutions work:

1. **Check Docker Desktop Logs**
   - Settings → Troubleshoot → View logs

2. **Reset Docker Desktop**
   - Settings → Troubleshoot → Reset to factory defaults
   - ⚠️ Warning: This will delete all containers and images

3. **Reinstall Docker Desktop**
   - Uninstall Docker Desktop
   - Download latest version from docker.com
   - Install and configure

4. **Alternative: Use WSL2 Backend**
   - Settings → General → Use WSL 2 based engine
   - Requires Windows 10/11 with WSL2 installed

## 🎓 Understanding the Issue

**Why This Happens:**

- Docker needs to download base images from Docker Hub
- Docker Hub is at `registry-1.docker.io`
- Your DNS server (1.1.1.1) is not responding
- Without DNS, Docker can't find Docker Hub
- Without Docker Hub, Docker can't download base images
- Without base images, Docker can't build your images

**The Fix:**

- Configure Docker to use working DNS servers (8.8.8.8, 8.8.4.4)
- These are Google's public DNS servers
- They're reliable and fast
- Once DNS works, everything else will work

---

**Next Step:** Try Solution 1 (Docker Desktop DNS configuration) and let me know the result!
