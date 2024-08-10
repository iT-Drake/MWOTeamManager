### Running server as a daemon on Ubuntu

A daemon is a long-running background process that is not under the control of a terminal. Here are the steps to set up your Waitress server as a daemon:
1. **Create a Systemd Service File**: Systemd is the default init system in Ubuntu, responsible for managing system services and daemons. You need to create a service file that describes your Waitress server.

   - Create a new file: `/etc/systemd/system/waitress.service`
   - Add the following content:
     ```
     [Unit]
     Description=Waitress Server Daemon
     After=network.target

     [Service]
     Type=simple
     User=<YourUserName>
     WorkingDirectory=<ProjectDirectory>
     ExecStart=<ProjectDirectory>/.venv/bin/waitress-serve --port <Port> --call website:create_app
     Restart=always

     [Install]
     WantedBy=multi-user.target
     ```

   Replace `YourUserName` with your actual username, and adjust the path `ProjectDirectory` accordingly.

2. **Set Correct Permissions**: Ensure that the service file has the correct permissions:
   ```bash
   sudo chmod 644 /etc/systemd/system/waitress.service
   ```

3. **Reload Systemd**: After creating the service file, you need to reload the systemd manager configuration:
   ```bash
   sudo systemctl daemon-reload
   ```

4. **Start and Enable the Service**: Now, you can start the Waitress server as a daemon and enable it to start on boot:
   ```bash
   sudo systemctl start waitress
   sudo systemctl enable waitress
   ```

5. **Check the Status**: To verify that your Waitress server is running as a daemon, use the following command:
   ```bash
   sudo systemctl status waitress
   ```

6. **Dig into the errors**: If you'll encounter any errors, you can check the log of the service with the following command:
   ```bash
   sudo journalctl -u waitress.naff.service
   ```

By following these steps, your Waitress server will run in the background as a daemon, and it will automatically start when the system boots.
You can manage the daemon using the `systemctl` command (e.g., `start`, `stop`, `restart`, `status`).

Remember to replace the placeholders in the service file with the appropriate paths and settings for your specific Waitress application.
