import axios from "axios";
import { useEffect, useState } from "react";
import ColumnsTable from "./ColumnsTable";

export const DataTable = (props) => {
  const { schemaName, title } = props;
  const [data, setData] = useState([]);
  const columnsData = data.length > 0 ? Object.keys(data[0]).map((key) => ({Header : key.toUpperCase(), accessor: key})) : [];

  useEffect(() => {
    schemaName &&
      axios
        .get(`http://localhost:5000/${schemaName}`)
        .then((response) => response.data)
        .then((json) => {
          if (typeof json === "string") {
            json = JSON.parse(json);
          }
          setData(json);
        })
        .catch((err) => console.log(err));
  }, [schemaName]);

  return data?.length > 0 ? <ColumnsTable columnsData={columnsData} tableData={data} title={title} {...props}/> : null;
};
