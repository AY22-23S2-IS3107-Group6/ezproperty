import React from 'react'

// Chakra imports
import { Box, Checkbox, SimpleGrid, Flex, Text, useColorModeValue } from "@chakra-ui/react";
import { graphs } from "data/ref";
import { useState } from "react";
import { PropertyCharts } from "views/admin/dataTables/components/PropertyCharts";

// Custom components
import Card from "components/card/Card.js";

const Charts = (props) => {
  const { ...rest } = props;
  const textColor = useColorModeValue("secondaryGray.900", "white");
  const [shownGraphs, setShownGraphs] = useState(
    graphs.map((obj) => ({ ...obj, show: false }))
  );

  const handleToggle = (selectedPropertyType, checked) => {
    setShownGraphs((prev) => {
      const { ...rest } = prev.find(
        (obj) => obj.propertyType === selectedPropertyType
      );
      return [
        ...prev.filter((obj) => obj.propertyType !== selectedPropertyType),
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
              Graph Selector
            </Text>
          </Flex>
          <SimpleGrid columns={{ base: 3 }}>
            {graphs.map(({ propertyType }) => (
              <Flex mb="20px" key={propertyType}>
                <Checkbox
                  me="16px"
                  colorScheme="brandScheme"
                  onChange={(e) => handleToggle(propertyType, e.target.checked)}
                />
                <Text
                  fontWeight="bold"
                  color={textColor}
                  fontSize="md"
                  textAlign="start"
                >
                  {propertyType}
                </Text>
              </Flex>
            ))}
          </SimpleGrid>
        </Card>
        {console.log(shownGraphs)}
        {shownGraphs.map(
          ({ propertyType, show }) =>
            show && (
              <PropertyCharts
                propertyType={propertyType}
              />
            )
        )}
      </SimpleGrid>
    </Box>
  );
}

export default Charts;