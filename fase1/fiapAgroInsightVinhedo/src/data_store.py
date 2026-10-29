crop_records = []

def add_record(record):
    crop_records.append(record)

def list_records():
    return crop_records

def update_record(index, new_record):
    if 0 <= index < len(crop_records):
        crop_records[index] = new_record
        return True
    return False

def delete_record(index):
    if 0 <= index < len(crop_records):
        del crop_records[index]
        return True
    return False