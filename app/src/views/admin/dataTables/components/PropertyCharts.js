import React from 'react';
import { Box, SimpleGrid, Flex, Text, useColorModeValue } from "@chakra-ui/react";
import Card from "components/card/Card.js";
import { LineChart } from "views/admin/dataTables/components/LineChart";
import { BarChart } from "views/admin/dataTables/components/BarChart";

export const PropertyCharts = (props) => {
  const { propertyType } = props;
  const textColor = useColorModeValue("secondaryGray.900", "white");

  return (
    <Box>
      <SimpleGrid columns={{ base: 1, md: 1, xl: 2 }} gap='20px'>
        <Card align='center' direction='column' w='100%'>
          <Flex justify='space-between' align='start' px='10px' pt='5px'>
            <Flex flexDirection='column' align='start' me='20px'>
              <Flex align='end'>
                <Text
                  color={textColor}
                  fontSize='25px'
                  fontWeight='700'
                  lineHeight='100%'>
                  Average Property Prices over Time
                </Text>
              </Flex>
            </Flex>
          </Flex>
          <Flex justify='space-between' align='start' px='10px' pt='5px'>
            <Flex flexDirection='column' align='start' me='20px'>
              <Flex align='end'>
                <Text
                  color={textColor}
                  fontSize='16px'
                  fontWeight= '300'
                  lineHeight='150%'>
                  For {propertyType}
                </Text>
              </Flex>
            </Flex>
          </Flex>
          <SimpleGrid
            mb="10px"
          ></SimpleGrid>
          <Box h='290px' mt='auto'>
            <LineChart
              propertyType={propertyType}
            />
          </Box>
        </Card>
        <Card align='center' direction='column' w='100%'>
          <Flex justify='space-between' align='start' px='10px' pt='5px'>
            <Flex flexDirection='column' align='start' me='20px'>
              <Flex align='end'>
                <Text
                  color={textColor}
                  fontSize='25px'
                  fontWeight='700'
                  lineHeight='100%'>
                  Top Average Property Price by District
                </Text>
              </Flex>
            </Flex>
          </Flex>
          <Flex justify='space-between' align='start' px='10px' pt='5px'>
            <Flex flexDirection='column' align='start' me='20px'>
              <Flex align='end'>
                <Text
                  color={textColor}
                  fontSize='16px'
                  fontWeight= '300'
                  lineHeight='150%'>
                  For {propertyType}
                </Text>
              </Flex>
            </Flex>
          </Flex>
          <SimpleGrid
            mb="10px"
          ></SimpleGrid>
          <Box h='290px' mt='auto'>
            <BarChart
              propertyType={propertyType}
            />
          </Box>
        </Card>
      </SimpleGrid>
    </Box>
  );
};
