import { useEffect, useState } from "react";
import axios from "axios";
import { Box, SimpleGrid } from "@chakra-ui/react";
import ColumnsTable from "views/admin/dataTables/components/ColumnsTable";
import { propertyInformationColumns } from "data/ref";
import { trainStationColumns } from "data/ref";

const Search = (props) => {
  const [propInfo, setPropInfo] = useState([]);
  const [trainStations, setTrainStations] = useState([]);

  useEffect(() => {
    // axios.get("http://localhost:5000/propertyinfo")
    //   .then(response => response.data)
    //   .then(data => setPropInfo(JSON.parse(data)))
    //   .catch(err => console.log(err));
    
    axios.get("http://localhost:5000/trainstation")
      .then(response => response.data)
      .then(data => {
        if(typeof(data) === "string"){
          data = JSON.parse(data)
        }
        setTrainStations(data)
      })
      .catch(err => console.log(err));
  }, []);

  return (
    <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
      <SimpleGrid
        columns={{ base: 1, "2xl": 2 }}
        gap="20px"
        mb="20px"
      >
        <ColumnsTable columnsData={propertyInformationColumns} tableData={propInfo} title={"Property Information"} />
        <ColumnsTable columnsData={trainStationColumns} tableData={trainStations} title={"Amenities: Train Stations"} />
      </SimpleGrid>
    </Box>
  );
};

export default Search;
