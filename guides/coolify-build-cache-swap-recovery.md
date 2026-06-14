# Recovering Coolify Deployments Failing During Docker Image Export

Use this when a Coolify deployment reaches Docker image build/export and then fails with errors like:

```text
Deployment failed: Command execution failed
exporting to image
failed to write compressed diff
context canceled
Build cache usage: ...GB
Reclaimable: ...GB
```

This usually means Docker/BuildKit cache pressure, too many old images, or low memory headroom. On small VPSs, missing swap can make Chromium or Playwright-heavy builds much less reliable.

## 1. Stop Deployment Retries

Before cleaning anything, stop clicking redeploy in Coolify. Repeated failed builds can create more cache and more unused images.

## 2. Check Server State

Run these on the Coolify server:

```bash
hostname
df -hT
df -ih
free -h
swapon --show
uptime
docker system df -v
docker builder du
```

Check Docker and kernel logs around the failed deployment:

```bash
sudo journalctl -u docker --since "10 minutes ago" --no-pager | tail -n 200
sudo journalctl -k --since "10 minutes ago" --no-pager | grep -Ei "oom|killed|no space|overlay|docker|buildkit|context canceled"
```

Important signs:

- `Build cache usage` is very large and `Reclaimable` is close to the same size: prune BuildKit.
- Many old images for the same Coolify resource have `CONTAINERS` set to `0`: prune unused images.
- `Swap: 0B`: add swap before retrying heavy builds.
- Kernel logs mention `oom` or `killed`: memory pressure is confirmed.
- Logs mention `no space left on device`: disk pressure is confirmed.

## 3. Safe Docker Cleanup

These commands remove build cache, unused images, and stopped containers. They do not delete running containers.

```bash
docker builder prune --all --force
docker image prune --all --force
docker container prune --force
```

Do not run `docker volume prune` unless you have confirmed the volumes are unused. Database data often lives in Docker volumes.

Check the result:

```bash
df -hT
docker system df
docker builder du
```

## 4. Add Swap

If `free -h` shows `Swap: 0B`, add an 8 GB swap file:

```bash
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Persist it across reboots:

```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Verify:

```bash
free -h
swapon --show
```

## 5. Retry Once

Retry the Coolify deployment once.

If it succeeds, check that the new app container is running and healthy in Coolify.

If it fails again, do not keep retrying. Collect fresh logs immediately:

```bash
sudo journalctl -u docker --since "10 minutes ago" --no-pager | tail -n 250
sudo journalctl -k --since "10 minutes ago" --no-pager | grep -Ei "oom|killed|no space|overlay|docker|buildkit|context canceled"
docker system df
docker builder du
```

## 6. When Cleanup Is Not Enough

If the server still fails at `exporting to image` after cache cleanup and swap:

- Restart Docker during a maintenance window:

```bash
sudo systemctl restart docker
```

- Retry one deployment.
- If the app image is very large, reduce the app image footprint in the repository. Common causes are browser binaries, Playwright/Chromium installs, dev dependencies copied into the runtime image, and repeated `COPY . /app` layers.
- If several deployments run at once, reduce Coolify deployment concurrency to one build at a time.

## Notes

- BuildKit cache can usually be deleted safely; it only makes future builds less cached.
- Unused images can usually be deleted safely; running containers keep their current images.
- Volumes are different. Treat volumes as persistent data until proven otherwise.
- A Playwright/Chromium production image can easily be several gigabytes, so old images accumulate quickly.
