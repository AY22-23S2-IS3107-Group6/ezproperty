import React from "react";

import { Icon } from "@chakra-ui/react";
import {
  MdAdd,
  MdHome,
  MdBarChart,
} from "react-icons/md";

import MainDashboard from "views/admin/default";
import View from "views/main/default";
import PropertyForm from "views/main/form";
import Charts from "views/main/charts";

const routes = [
  {
    name: "Main Dashboard",
    layout: "/admin",
    path: "/default",
    icon: <Icon as={MdHome} width='20px' height='20px' color='inherit' />,
    component: View,
  },
  {
    name: "Charts",
    layout: "/admin",
    path: "/charts",
    icon: <Icon as={MdBarChart} width='20px' height='20px' color='inherit' />,
    component: Charts,
  },
  {
    name: "Add Property Tranasction",
    layout: "/admin",
    path: "/add-property",
    icon: <Icon as={MdAdd} width='20px' height='20px' color='inherit' />,
    component: PropertyForm,
  },
  {
    name: "Template",
    layout: "/admin",
    path: "/template",
    icon: <Icon as={MdHome} width='20px' height='20px' color='inherit' />,
    component: MainDashboard,
  },
  // {
  //   name: "NFT Marketplace",
  //   layout: "/admin",
  //   path: "/nft-marketplace",
  //   icon: (
  //     <Icon
  //       as={MdOutlineShoppingCart}
  //       width='20px'
  //       height='20px'
  //       color='inherit'
  //     />
  //   ),
  //   component: NFTMarketplace,
  //   secondary: true,
  // },
  // {
  //   name: "Data Tables",
  //   layout: "/admin",
  //   icon: <Icon as={MdBarChart} width='20px' height='20px' color='inherit' />,
  //   path: "/data-tables",
  //   component: DataTables,
  // },
  // {
  //   name: "Profile",
  //   layout: "/admin",
  //   path: "/profile",
  //   icon: <Icon as={MdPerson} width='20px' height='20px' color='inherit' />,
  //   component: Profile,
  // },
  // {
  //   name: "Sign In",
  //   layout: "/auth",
  //   path: "/sign-in",
  //   icon: <Icon as={MdLock} width='20px' height='20px' color='inherit' />,
  //   component: SignInCentered,
  // },
  // {
  //   name: "RTL Admin",
  //   layout: "/rtl",
  //   path: "/rtl-default",
  //   icon: <Icon as={MdHome} width='20px' height='20px' color='inherit' />,
  //   component: RTL,
  // },
];

export default routes;
