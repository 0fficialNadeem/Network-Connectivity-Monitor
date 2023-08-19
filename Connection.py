import socket
import datetime
import os
import time

# Get the current working directory
CWD = os.getcwd()

# Define the filepath for the network log file
FILEPATH = os.path.join(CWD, "NetworkLog.txt")


def main():
    # Flag to track the first check for an Internet connection
    firstcheck = False

    # Flag to track the first check for an Internet connection
    started_monitoring = datetime.datetime.now()

    # Flag to track the first check for an Internet connection
    first_check_failed = False

    while True:
        # An initial check for an Internet Connection
        if firstcheck == False:
            if first_check() == False:
                first_check_failed = True
            log_msg = (
                f"Started Monitoring at: {str(started_monitoring).split('.')[0]}\n"
            )
            with open(FILEPATH, "a") as file:
                file.write(log_msg)
            firstcheck = True
        else:
            # First check completed, so now continuously check for connection
            has_disconnected = False
            if not first_check_failed:
                disconnected_time = datetime.datetime.now()
            else:
                disconnected_time = started_monitoring

            while True:
                # If not connected
                time.sleep(1)
                if not has_disconnected and not ping("www.google.com"):
                    if not first_check_failed:
                        # Get disconnected time
                        disconnected_time = datetime.datetime.now()
                        # Log this message to the file
                        log_msg = (
                            f"Disconnected at: {str(disconnected_time).split('.')[0]}\n"
                        )
                        with open(FILEPATH, "a") as file:
                            file.write(log_msg)
                    has_disconnected = True

                # If reconnected
                if has_disconnected and ping("www.google.com"):
                    # Get time it reconnected and log it, including downtime
                    reconnecion_time = datetime.datetime.now()
                    log_msg = f"Reconnected at: {str(reconnecion_time).split('.')[0]}\n"
                    downtime = calculate_downtime(reconnecion_time, disconnected_time)
                    with open(FILEPATH, "a") as file:
                        file.write(log_msg)
                        file.write(
                            f"Connection was unavailable for {str(downtime).split('.')[0]}\n"
                        )
                    has_disconnected = False
                first_check_failed = False


# Calculates downtime
def calculate_downtime(reconnected_time, disconnected_time):
    difference = reconnected_time - disconnected_time
    return str(difference).split(".")[0]


# Establish Connection with server
# If machine does not recieve any packets then it has no live internet connection
def ping(domain):
    PORT = 80
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Socket Creation Unsuccessful")
        return False
    else:
        try:
            HOST_IP = socket.gethostbyname(domain)
        except socket.gaierror:
            print("there was an error resolving the host")
            return False
        else:
            s.connect((HOST_IP, PORT))
            return True


# Defined for an initial check for an Internet Connection
def first_check():
    time = datetime.datetime.now()
    if ping("www.google.com"):
        status = "CONNECTION ACQUIRED\n\n"
        log_msg = f"Connection made at: {str(time).split('.')[0]}\n"

        with open(FILEPATH, "a") as file:
            file.write(status)
            file.write(log_msg)
        return True
    else:
        status = "CONNECTION FAILED\n\n"
        log_msg = f"Disconnected at: {str(time).split('.')[0]}\n"

        with open(FILEPATH, "a") as file:
            file.write(status)
            file.write(log_msg)
        return False


if __name__ == "__main__":
    main()
