import React from 'react'

// Chakra imports
import { Box, Checkbox, SimpleGrid, Flex, Text, useColorModeValue, Image } from "@chakra-ui/react";
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
        <SimpleGrid columns={{ base: 1, md: 1, xl: 2 }} gap='20px'>
          <Card
            p="20px"
            align="center"
            direction="column"
            w="100%"
            {...rest}
            width={2}
          >
            <Flex alignItems="center" w="100%" mb="30px">
              <Text color={textColor} fontSize="2xl" fontWeight="700">
                Graph Selector
              </Text>
            </Flex>
            <SimpleGrid columns={{ base: 2 }} gap="15px">
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
                    fontSize="xl"
                    textAlign="start"
                  >
                    {propertyType}
                  </Text>
                </Flex>
              ))}
            </SimpleGrid>
          </Card>
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
                District Map
              </Text>
            </Flex>
            <Image
              src = 'https://www.mingproperty.sg/wp-content/uploads/2015/10/SingaporeDistrictCode-MapDemarcation624x350.png'
              alt = ''
            />
          </Card>
        </SimpleGrid>
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