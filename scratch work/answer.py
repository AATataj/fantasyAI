presetDrivers = []
leftoverDrivers = []
solvedVehicles = []

youngest = drivers[0]
oldest = vehicles[0]

switchableDr = True
switchableV = False


## partition the list into drivers with principle vehicles already attached and not
for driv in drivers :
    if driv.principleVehicle !='':
        presetDrivers.append(driv)
    else:
        leftoverDrivers.append(driv)
    if driv.age < youngest.age:
        youngest = driv
        youngestIndex = drivers.index(driv)

## assign vehicles with principle drivers already attached and remove 
## those vehicles from the master list
for driv in presetDrivers:
    for vehicle in vehicles:
        if driv.age == youngest.age:
            switchableDr = False
            youngestIndex = preserDrivers.index(driv)
        if oldest.year > vehicle.year:
            oldest = vehicle.year
        if vehicle.ID = presetDrivers.principleVehicle:
            vehicle.driverIDs.append(driv)
            solvedVehicles.append(vehicle)
            vehicles.remove(vehicle)

## assign drivers with no principle vehicle to vehicles with no primary driver
for x in range (len(leftoverDrivers)):
    if oldest.year == vehicles.year:
        switchableV = True 
    ## case where we have vehicles left
    if len(vehicles) > 0:
        leftoverDrivers[x].principleVehicle = vehicles[0].ID
        vehicles[0].driverIDs.append(leftoverDrivers[x])
        solvedVehicles.append(vehicles[0])
        vehicles.remove(vehicles[0])
    ## case where we've run out of vehicles
    else :
        leftoverDrivers[x].principleVehicle = solvedVehicles[0].ID
        solvedVehicles[0].driverIDs.append(leftoverDrivers[x])

## assign oldest car to youngest driver if possible
drivers = presetDrivers.append(leftoverDrivers)
vehicles = solvedVehicles
if switchableV and switchableDr:
    vehicleIndex = vehicles.index(oldest)
    driverIndex = drivers.index(youngest)
    tempVehicleID = driver.principleVehicle
    tempDrivID = vehicle.driverIDs[0]
    driver.principleVehicle = vehicle.ID
    vehicle.driverIDs[0] = driver.ID
    for driver in drivers:
        if driver.ID == tempDrivID
            for vehicle in vehicles:
                if vehicle.ID == tempVehicleID:
                    vehicle.driverIDs[0]=driver.ID
                    driver.principleVehicle = vehicle.ID

## optimal, yes.
switchableDriver = False
switchableVehicle = False
for i in range(len(vehicles)):
    if vehicles.year < oldest.year:
        oldest = vehicles[i]
        oldestIndex = i
    for j in range(len(drivers)):
        if drivers[j].age < youngest.age:
            youngest = drivers[j]
            youngestIndex = j
        ## case with predetermined principle vehicles
        if drivers[j].principleVehicle == vehicles[i].ID:
            vehicles[i].driverIDs.append(driver[i].ID)
            continue
        ## case for empty in both:
        elif drivers[j].principleVehicle =='' and len(vehicles[i].driverIDs) == 0:
            vehicles[i].driverIDs.append(driver[i].ID)
            drivers[j].principleVehicle = vehicles[i].ID 
        ## case where we run out of vehicles
        elif drivers[i].principleVehicle == '' and len(vehicles[j].driverIDs) > 0:
            vehicles[j].driverIDs.append(driver[i].ID)
            driver[i].principleVehicle = vehicles[j].ID
        ## case where we have too many vehicles
        elif len(driver) < len(vehicle) and (i-1) == len(driver) and vehicle.driverIDs == []:
            vehicles[j].driverIDs.append(driver[i].ID)
        ## figure out if and who to switch principle vehicles with    
        if i == youngestIndex:
                switchableVehicleIndex = j
                switchableDriver = True
        if j == oldestIndex:
                switchableDriverIndex = i
                switchableVehicle = True
if switchableVehicle and switchableDriver:
    tempVehicleID = drivers[youngestIndex].principleVehicle
    tempDriverID = vehicles[oldestIndex].driverIDs[0]
    drivers[youngestIndex].principleVehicle = vehicles[oldestIndex].ID
    vehicles[oldestIndex].driverIDs[0] = drivers[youngestIndex].ID
    drivers[switchableDriverIndex].principleVehicle = tempVehicleID
    vehicles[switchableVehicleIndex].driverIDs[0] = tempDriverID





"""
for driv in drivers:
    if driv.age < youngest.age:
        youngest = driv 
    if driv.principleVehicle != '':
        if youngest.age = drive.age:
            switchableDr = False
        for vehicle in vehicles:
            if vehicle.year < oldest.year:
                oldest = vehicle
            if vehicle.vehicleID = driv.principleVehicle:
                vehicle.driverIDs.append(driv.ID)
                if vehicle.year == oldest.year :
                    switchableV = False
    elif driv.principleVehicle == '':
        if youngest.age = drive.age:
            switchableDr = True
        for vehicle in vehicles:
            if vehicle.year < oldest.year:
                oldest = vehicle
            if vehicle.driverIDs == []:
                driv.principleVehicle = vehicle.vehicleID
                vehicle.driverIDs.append(driv.ID)
            if vehicle.year == oldest.year :
                switchableV = True
if switchableDr and switchableV:
    for driver in drivers:
        if driver.age == youngest.age:
            driver.principleVehicle = oldest.vehicleID
            for vehicle in vehicles:
                if oldest.year == vehicle.year:
                    vehicle.driverIds[len(vehicle.driverIDs)] = youngest.driverID  
"""

        
