import {
  Box,
  Checkbox,
  Flex,
  SimpleGrid,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import Card from "components/card/Card";
import { tables } from "data/ref";
import { useState } from "react";
import { DataTable } from "views/admin/dataTables/components/DataTable";

const Search = (props) => {
  const { ...rest } = props;
  const textColor = useColorModeValue("secondaryGray.900", "white");
  const [shownTables, setShownTables] = useState(
    tables.map((obj) => ({ ...obj, show: false }))
  );

  const handleToggle = (selectedSchemaName, checked) => {
    setShownTables((prev) => {
      const { ...rest } = prev.find(
        (obj) => obj.schemaName === selectedSchemaName
      );
      return [
        ...prev.filter((obj) => obj.schemaName !== selectedSchemaName),
        { ...rest, show: checked },
      ];
    });
  };

  return (
    <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
      <SimpleGrid columns={{ base: 1 }} gap="20px" mb="20px">
        <Card
          p="20px"
          align="center"
          direction="column"
          w="100%"
          {...rest}
          width={2}
        >
          <Flex alignItems="center" w="100%" mb="30px">
            <Text color={textColor} fontSize="lg" fontWeight="700">
              Table Selector
            </Text>
          </Flex>
          <SimpleGrid columns={{ base: 3 }}>
            {tables.map(({ schemaName, title }) => (
              <Flex mb="20px" key={schemaName}>
                <Checkbox
                  me="16px"
                  colorScheme="brandScheme"
                  onChange={(e) => handleToggle(schemaName, e.target.checked)}
                />
                <Text
                  fontWeight="bold"
                  color={textColor}
                  fontSize="md"
                  textAlign="start"
                >
                  {title}
                </Text>
              </Flex>
            ))}
          </SimpleGrid>
        </Card>
        {console.log(shownTables)}
        {shownTables.map(
          ({ schemaName, title, show }) =>
            show && (
              <DataTable
                key={schemaName}
                schemaName={schemaName}
                title={title}
              />
            )
        )}
      </SimpleGrid>
    </Box>
  );
};

export default Search;
