from crontab import CronTab


def add_cron(job_name, curl_command, date_time):
    """
    Adds a new cron job to execute a curl command at a specific date-time.

    Args:
        job_name (str): A unique name for the cron job (used for identification).
        curl_command (str): The full curl command to execute.
        date_time (str): The execution date-time in "YYYY-MM-DD HH:MM" format.
    """
    cron = CronTab(user=True)

    # Parse date_time
    from datetime import datetime
    dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M")

    # Create a cron job
    job = cron.new(command=curl_command, comment=job_name)
    job.setall(dt.minute, dt.hour, dt.day, dt.month, '*')

    cron.write()
    print(f"Cron job '{job_name}' added to run at {date_time}")


def remove_cron(job_name):
    """
    Removes a cron job by its unique name (comment).

    Args:
        job_name (str): The name of the cron job to remove.
    """
    cron = CronTab(user=True)
    jobs_removed = cron.remove_all(comment=job_name)

    if jobs_removed:
        cron.write()
        print(f"Cron job '{job_name}' removed.")
    else:
        print(f"No cron job found with the name '{job_name}'.")


def list_crons():
    """
    Lists all current cron jobs for the user.
    """
    cron = CronTab(user=True)
    for job in cron:
        print(job)


# Example Usage
if __name__ == "__main__":
    # Replace with your use cases
    add_cron("example_job", "curl -X GET https://example.com", "2024-12-06 15:30")
    list_crons()
    remove_cron("example_job")