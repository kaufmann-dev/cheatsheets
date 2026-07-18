# Preserving Coolify Runtime Logs with Axiom

Use this guide only if a Coolify application again enters an unexplained restart loop and its runtime logs disappear after the container stops.

Do not configure this preemptively for a single transient incident that resolved after redeployment. A successful deployment only proves that Coolify built or reused an image and launched a container; it does not prove that the application process remained running.

Axiom is a hosted logging service at [app.axiom.co](https://app.axiom.co/). It does not run inside Coolify. Coolify forwards container output to Axiom so the logs remain available after an exited container is removed.

## 1. Confirm This Guide Applies

Use Axiom log retention when all of the following are true:

- The Coolify application status is `Exited` or repeatedly restarting.
- The public domain shows `no available server`.
- The deployment itself is marked successful, or the build log does not contain the runtime exception.
- The Coolify **Logs** page becomes empty after the stopped container is removed.
- Restarting or redeploying restores the application without explaining the original failure.

If the container remains running but is marked unhealthy, investigate the health check, exposed port, and listening address instead. If the deployment build fails, inspect the deployment log rather than configuring a runtime log drain.

## 2. Create an Axiom Account

1. Open [app.axiom.co](https://app.axiom.co/).
2. Create an account and organization.
3. Select **EU Central 1** when Axiom asks for an edge deployment or region.

## 3. Create a Dataset

In Axiom:

1. Open **Settings**.
2. Select **Datasets and views**.
3. Click **New dataset**.
4. Configure:
   - **Name:** `<application-name>-production`, for example `jobstrian-production`
   - **Kind:** `Events`
   - **Description:** `Coolify runtime logs for <application-name>`
   - **Data retention:** the shortest period sufficient for incident diagnosis, normally 7 to 30 days
   - **Edge deployment:** `EU Central 1`
5. Click **Save dataset**.

Axiom dataset documentation: <https://axiom.co/docs/reference/datasets>

## 4. Create a Restricted Ingest Token

In Axiom:

1. Open **Settings → API tokens**.
2. Click **New API token**.
3. Set the name to `coolify-<application-name>-ingest`.
4. Add a description such as `Allows Coolify to send <application-name> logs`.
5. Under **Token permissions**, select **Basic**.
6. Under **Dataset access**, select only the dataset created in the previous step.
7. Click **Create**.
8. Copy the token immediately and keep it secure. Axiom does not display it again.

Do not use a Personal Access Token. A PAT grants unnecessary control over the Axiom account. The basic API token needs ingest access only to the selected dataset.

Axiom token documentation: <https://axiom.co/docs/reference/tokens>

## 5. Configure the Server-Level Log Drain in Coolify

In Coolify:

1. Open **Servers**.
2. Select the server hosting the affected application, such as **localhost**.
3. Open **Log Drains**.
4. Add or enable an **Axiom** log drain.
5. Enter the Axiom dataset name and the restricted API token.
6. Save the configuration.

Keep the Axiom token only in Coolify's Log Drain configuration. Do not add it to the application repository, `.env.example`, `nixpacks.toml`, or the application's runtime environment variables.

## 6. Enable the Drain for the Application

1. Open the affected application in Coolify.
2. Open **Configuration → Advanced**.
3. Enable **Drain Logs**.
4. Save the setting.
5. Restart or redeploy the application once. Coolify requires a restart before log-drain changes take effect.

Coolify Log Drain documentation: <https://coolify.io/docs/knowledge-base/drain-logs>

## 7. Verify Log Delivery

1. Wait approximately one minute after the restart.
2. Open the dataset in Axiom.
3. Open **Stream**, **Live Tail**, or **Explore**, depending on the current Axiom navigation.
4. Set the time range to the last 15 minutes.
5. Confirm that the application's container or startup messages appear.

If no events appear:

- Confirm that the Axiom drain is enabled under the hosting server's **Log Drains** page.
- Confirm that **Drain Logs** is enabled on the application resource.
- Confirm that the application was restarted after both settings were enabled.
- Confirm that the token is a basic API token with access to the correct dataset.
- Confirm that the dataset name in Coolify exactly matches the Axiom dataset.

## 8. Diagnose the Next Restart Loop

When the failure happens again:

1. Record the incident time and timezone.
2. In Axiom, filter the dataset to a window beginning several minutes before the first restart and ending after the final exit.
3. Find the first error or exception, not only the repeated shutdown messages.
4. Export or copy the complete exception and stack trace, redacting credentials and personal data.
5. Classify the failure before changing the application:
   - PostgreSQL connectivity, DNS, credentials, or TLS
   - database migration failure
   - missing or invalid runtime environment variable
   - memory or other resource exhaustion
   - application or Node.js exception
   - health-check, exposed-port, or proxy configuration failure
6. Apply a correction only to the failing layer. For example, add bounded database-startup retries only if the retained logs prove that a transient database connection failure caused the exits.

Do not disable health checks, change ports, alter migrations, or add broad retry loops solely because the public page displayed `no available server`. That message means the proxy had no healthy backend; it is not the underlying error.

## Security and Cost Notes

- Container logs can contain URLs, database errors, email addresses, or other sensitive operational data. Review what the application logs and choose an appropriate retention period.
- Never paste the Axiom API token into issue trackers, chat messages, source control, or diagnostic output.
- Restrict the token to a single dataset and rotate it if it is exposed.
- Delete or disable the log drain when it is no longer needed if ongoing external log retention is undesirable.
