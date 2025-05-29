def lookup_records(filters):
    # Code to lookup records based on filters
    pass

def archive_records(filters):
    # Code to archive records based on filters
    pass

def database_maintenance():
    print("Please provide filters for record lookup:")
    lookup_filters = input("Enter lookup filters: ")

    print("\nPerforming record lookup with filters:", lookup_filters)
    lookup_records(lookup_filters)

    print("\nPlease provide filters for record archival:")
    archive_filters = input("Enter archival filters: ")

    print("\nPerforming record archival with filters:", archive_filters)
    archive_records(archive_filters)

# Main program
database_maintenance()